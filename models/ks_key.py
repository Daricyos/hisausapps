import logging

from odoo import models, fields

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
        print(params)
        res = api.get_ruling_all(params=params)
        self.load_rulings(res)

    def load_rulings(self, data):
        ruling_m = self.env['ks.hisa.ruling']
        for item in data:
            data_to_create = {
                'hisa_ruling_id': item['hisaRulingId'],
                'action_code': item['actionCode'],
                'customCode': item['customCode'],
                'location_id': item['locationId'],
                'persons_involved_ids': [(6, 0, self.get_persons_inv_from_data(item['personsInvolved']))]
            }
            rul_id = ruling_m.search([('hisa_ruling_id', '=', item['hisaRulingId'])])
            if rul_id:
                ruling_m.write(data_to_create)
            else:
                ruling_m.create(data_to_create)

    def get_persons_inv_from_data(self, data):
        persons_ids = []
        for item in data:
            pers_to_create = {
                'hisa_person_id': item['hisaPersonId'],
                'person_name': item['personName'],
            }
            per_id = self.env['ks.hisa.ruling.persons.involved'].create(pers_to_create)
            persons_ids.append(per_id.id)
        return persons_ids


