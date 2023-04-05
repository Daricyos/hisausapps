import base64
import logging

from odoo import models, fields
import datetime

from .hisa import HisaAPI

_logger = logging.getLogger()


class KeyHisausapps(models.Model):
    _name = 'ks.hisa.key'
    _description = 'Ks Hisa Key'

    name = fields.Char()
    key = fields.Char()

    ruling_all_text = fields.Char(default=' ', )
    ruling_all_page = fields.Integer()
    ruling_all_page_size = fields.Integer()
    ruling_all_sort_by = fields.Char()
    ruling_all_sort_direction = fields.Integer()

    def button_get_ruling_all(self):
        self.ensure_one()
        api = HisaAPI(key=self.key, )
        params = {
            'text': self.ruling_all_text,
            'pageSize': self.ruling_all_page_size,
        }
        if self.ruling_all_page:
            params['page'] = self.ruling_all_page
        if self.ruling_all_sort_by:
            params['sortBy'] = self.ruling_all_sort_by
        if self.ruling_all_sort_direction:
            params['sortDirection'] = self.ruling_all_sort_direction
        res = api.get_ruling_all(params=params)
        self.load_rulings(res, api)

    def load_rulings(self, data, api):
        ruling_m = self.env['ks.hisa.ruling']
        for item in data:
            data_to_create = {
                'hisa_ruling_id': item['hisaRulingId'],
                'action_code': item['actionCode'],
                'customCode': item['customCode'],
                'location_id': item['locationId'],
                'persons_involved_ids': [(6, 0, self.get_persons_inv_from_data(item['personsInvolved']))],
                # 'files_uri_ids': [(6, 0, self.get_files_from_url(item['filesUri'], api))]
            }
            rul_id = ruling_m.search([('hisa_ruling_id', '=', item['hisaRulingId'])])
            if rul_id:
                ruling_m.write(data_to_create)
            else:
                ruling_m.create(data_to_create)

    # def get_files_from_url(self, urls, api):
    #     docs_ids = []
    #     print(urls)
    #     for url in urls:
    #         response = api.get_file_from_ruling(url)
    #         doc_id = self.env['ks.hisa.files.uri'].create({
    #                 'name': url.split('/')[-1],
    #                 'res_field': url,
    #                 'datas': base64.b64encode(response.content).replace(b'\n', b'', )
    #             })
    #         docs_ids.append(doc_id.id)
    #     return docs_ids

    def get_persons_inv_from_data(self, data):
        persons_ids = []
        for item in data:
            print(item)
            pers_to_create = {
                'hisa_person_id': item['hisaPersonId'],
                'person_name': item['personName'],
                'fine_amount': item['fine']['amount'] if item['fine'] is not None else None,
                'fine_recovery_amount': item['fine']['costRecovery']['amount'] if item['fine'] is not None and item['fine']['costRecovery'] is not None else None,
                'fine_recovery_date': datetime.datetime.strptime(item['fine']['costRecovery']['dueDate'], "%Y-%m-%d").date() if item['fine'] is not None and item['fine']['costRecovery'] is not None else None,
                'fine_paid': item['fine']['paid'] if item['fine'] is not None else None,
                'fine_total': item['fine']['total'] if item['fine'] is not None else None,
                'fine_amount_paid': item['fine']['amountPaid'] if item['fine'] is not None else None,
                'fine_payment_due': datetime.datetime.strptime(item['fine']['paymentDue'], "%Y-%m-%d").date() if item['fine'] is not None else None,
                'fine_installments_ids': [(6, 0, self.get_persons_installments(item['fine']['installments']))] if item['fine'] is not None else None,
            }
            per_id = self.env['ks.hisa.ruling.persons.involved'].create(pers_to_create)
            persons_ids.append(per_id.id)
        return persons_ids

    def get_persons_installments(self, data):
        installments_ids = []
        for item in data:
            installments_to_create = {
                'installments_amount': item['fine']['installments']['amount'] if item['fine'] is not None and item['fine']['installments'] is not None else None,
                'installments_due_date': datetime.datetime.strptime(item['fine']['installments']['dueDate'], "%Y-%m-%d").date() if item['fine'] is not None and item['fine']['installments'] is not None else None,
            }
            inst_id = self.env['ks.hisa.installments'].create(installments_to_create)
            installments_ids.append(inst_id.id)
        return installments_ids


