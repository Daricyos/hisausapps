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

    def test_button(self):
        self.ensure_one()
        api = HisaAPI(key=self.key, )
        l = api.get_location_autocomplete('')
        print(l)

    def load_rulings(self, data, api):
        ruling_m = self.env['ks.hisa.ruling']
        for item in data:
            data_to_create = {
                'hisa_ruling_id': item['hisaRulingId'],
                'action_code': item['actionCode'],
                'customCode': item['customCode'],
                'location_id': item['locationId'],
                'persons_involved_ids': [(6, 0, self.get_persons_inv_from_data(item['personsInvolved']))],
                'horses_involved_ids': [(6, 0, self.get_horses_involved(item['horsesInvolved']))] if item[
                                                                                                         'horsesInvolved'] is not None else None,
                'adjudicators_hisa_board_id': item['adjudicatorsHisaId']['hisaBoard'] if item['adjudicatorsHisaId'] and
                                                                                         item['adjudicatorsHisaId'][
                                                                                             'hisaBoard'] is not None else None,
                'adjudicators_hisa_board_panel_id': item['adjudicatorsHisaId']['boardPanel'] if item[
                                                                                                    'adjudicatorsHisaId'] and
                                                                                                item[
                                                                                                    'adjudicatorsHisaId'][
                                                                                                    'boardPanel'] is not None else None,
                'adjudicators_hisa_arbitral_panel_id': item['adjudicatorsHisaId']['arbitralPanel'] if item[
                                                                                                          'adjudicatorsHisaId'] and
                                                                                                      item[
                                                                                                          'adjudicatorsHisaId'][
                                                                                                          'arbitralPanel'] is not None else None,
                'adjudicators_hisa_rsc_members_id': item['adjudicatorsHisaId']['rscMembers'] if item[
                                                                                                    'adjudicatorsHisaId'] and
                                                                                                item[
                                                                                                    'adjudicatorsHisaId'][
                                                                                                    'rscMembers'] is not None else None,
                'adjudicators_hisa_nsp_members_id': item['adjudicatorsHisaId']['nspMembers'] if item[
                                                                                                    'adjudicatorsHisaId'] and
                                                                                                item[
                                                                                                    'adjudicatorsHisaId'][
                                                                                                    'nspMembers'] is not None else None,
                'adjudicators_hisa_track_stewards_id': item['adjudicatorsHisaId']['trackStewards'] if item[
                                                                                                          'adjudicatorsHisaId'] and
                                                                                                      item[
                                                                                                          'adjudicatorsHisaId'][
                                                                                                          'trackStewards'] is not None else None,
                'status': item['status'],
                'stage': item['stage'],
                'ruling_body': item['rulingBody'] if item['rulingBody'] is not None else None,
                'can_be_appealed': item['canBeAppealed'] if item['canBeAppealed'] is not None else None,
                'ruling_date': item['rulingDate'] if item['rulingDate'] is not None else None,
                'date_entered': item['dateEntered'] if item['dateEntered'] is not None else None,
                'last_day_of_appeal': item['lastDayOfAppeal'] if item['lastDayOfAppeal'] is not None else None,
                'horse_id': item['horseId'] if item['horseId'] is not None else None,
                'race_number': item['raceNumber'] if item['raceNumber'] is not None else None,
                'responsible_person_hisaId': item['responsiblePersonHisaId'] if item[
                                                                                    'responsiblePersonHisaId'] is not None else None,
                'owner_hisa_id': item['ownerHisaId'] if item['ownerHisaId'] is not None else None,
                'classification': item['classification'] if item['classification'] is not None else None,
                'location_name': item['locationName'] if item['locationName'] is not None else None,
                'horse_name': item['horseName'] if item['horseName'] is not None else None,
                'responsible_person_name': item['responsiblePersonName'] if item[
                                                                                'responsiblePersonName'] is not None else None,
                'owner_name': item['ownerName'] if item['ownerName'] is not None else None,
                'status_display_name': item['statusDisplayName'] if item['statusDisplayName'] is not None else None,
                'reporting_date': item['reportingDate'] if item['reportingDate'] is not None else None,
                # 'files_uri_ids': [(6, 0, self.get_files_from_url(item['filesUri'], api))]
            }
            rul_id = ruling_m.search([('hisa_ruling_id', '=', item['hisaRulingId'])])
            if rul_id:
                ruling_m.write(data_to_create)
            else:
                ruling_m.create(data_to_create)
            is_location_true = self.env['my.location'].search(
                [('name', '=', data_to_create['location_name']), ('id_local_name', '=', data_to_create['location_id'])],
                limit=1)
            if not is_location_true:
                is_location_true.create({
                    'name': data_to_create['location_name'],
                    'id_local_name': data_to_create['location_id'],
                })

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
            pers_to_create = {
                'hisa_person_id': item['hisaPersonId'],
                'person_name': item['personName'],
                'fine_amount': item['fine']['amount'] if item['fine'] is not None else None,
                'fine_recovery_amount': item['fine']['costRecovery']['amount'] if item['fine'] is not None and
                                                                                  item['fine'][
                                                                                      'costRecovery'] is not None else None,
                'fine_recovery_date': datetime.datetime.strptime(item['fine']['costRecovery']['dueDate'],
                                                                 "%Y-%m-%d").date() if item['fine'] is not None and
                                                                                       item['fine'][
                                                                                           'costRecovery'] is not None else None,
                'fine_paid': item['fine']['paid'] if item['fine'] is not None else None,
                'fine_total': item['fine']['total'] if item['fine'] is not None else None,
                'fine_amount_paid': item['fine']['amountPaid'] if item['fine'] is not None else None,
                'fine_payment_due': datetime.datetime.strptime(item['fine']['paymentDue'], "%Y-%m-%d").date() if item[
                                                                                                                     'fine'] is not None else None,
                'fine_installments_ids': [(6, 0, self.get_persons_installments(item['fine']['installments']))] if item[
                                                                                                                      'fine'] is not None and
                                                                                                                  item[
                                                                                                                      'fine'][
                                                                                                                      'installments'] is not None else None,
                'suspension_start': item['suspension']['start'] if item['suspension'] is not None else None,
                'suspension_duration': item['suspension']['duration'] if item['suspension'] is not None else None,
                'suspension_dates_ids': [(6, 0, self.get_persons_suspension(item['suspension']['dates']))] if item[
                                                                                                                  'suspension'] is not None and
                                                                                                              item[
                                                                                                                  'suspension'][
                                                                                                                  'dates'] is not None else None,
                'points_amount': item['points']['amount'] if item['points'] and item['points'][
                    'amount'] is not None else None,
                'points_expire_date': item['points']['expireDate'] if item['points'] and item['points'][
                    'expireDate'] is not None else None,
                'points_duration': item['points']['duration'] if item['points'] and item['points'][
                    'duration'] is not None else None,
                'purse_forfeiture_percent_amount': item['purseForfeiturePercent']['amount'] if item[
                                                                                                   'purseForfeiturePercent'] and
                                                                                               item[
                                                                                                   'purseForfeiturePercent'][
                                                                                                   'amount'] is not None else None,
                'purse_forfeiture_percent_paid': item['purseForfeiturePercent']['paid'] if item[
                                                                                               'purseForfeiturePercent'] and
                                                                                           item[
                                                                                               'purseForfeiturePercent'][
                                                                                               'paid'] is not None else None,
                'purse_forfeiture_percent_disqualified': item['purseForfeiturePercent']['disqualified'] if item[
                                                                                                               'purseForfeiturePercent'] and
                                                                                                           item[
                                                                                                               'purseForfeiturePercent'][
                                                                                                               'disqualified'] is not None else None,
                'purse_forfeiture_percent_withheld': item['purseForfeiturePercent']['withheld'] if item[
                                                                                                       'purseForfeiturePercent'] and
                                                                                                   item[
                                                                                                       'purseForfeiturePercent'][
                                                                                                       'withheld'] is not None else None,
                'required_actions_description': item['requiredActions']['description'] if item['requiredActions'] and
                                                                                          item['requiredActions'][
                                                                                              'description'] is not None else None,
                'required_actions_completed': item['requiredActions']['completed'] if item['requiredActions'] and
                                                                                      item['requiredActions'][
                                                                                          'completed'] is not None else None,
                'required_actions_complete_by_date': item['requiredActions']['completeByDate'] if item[
                                                                                                      'requiredActions'] and
                                                                                                  item[
                                                                                                      'requiredActions'][
                                                                                                      'completeByDate'] is not None else None,
                'required_actions_fine_per_calendar_day': item['requiredActions']['finePerCalendarDay'] if item[
                                                                                                               'requiredActions'] and
                                                                                                           item[
                                                                                                               'requiredActions'][
                                                                                                               'finePerCalendarDay'] is not None else None,
                'details_regulation_number': item['details']['regulationNumber'] if item['details'] and item['details'][
                    'regulationNumber'] is not None else None,
                'details_description': item['details']['description'] if item['details'] and item['details'][
                    'description'] is not None else None,
                'details_stewards_ruling': item['details']['stewardsRuling'] if item['details'] and item['details'][
                    'stewardsRuling'] is not None else None,
                'details_rsc_ruling': item['details']['rscRuling'] if item['details'] and item['details'][
                    'rscRuling'] is not None else None,
                'details_nsp_ruling': item['details']['nspRuling'] if item['details'] and item['details'][
                    'nspRuling'] is not None else None,
                'details_arbitral_ruling': item['details']['arbitralRuling'] if item['details'] and item['details'][
                    'arbitralRuling'] is not None else None,
                'details_hisa_board_apeal_ruling': item['details']['hisaBoardApealRuling'] if item['details'] and
                                                                                              item['details'][
                                                                                                  'hisaBoardApealRuling'] is not None else None,
                'details_nsp_board_panel_ruling': item['details']['boardPanelRuling'] if item['details'] and
                                                                                         item['details'][
                                                                                             'boardPanelRuling'] is not None else None,
                'details_hisa_board_ruling': item['details']['hisaBoardRuling'] if item['details'] and item['details'][
                    'hisaBoardRuling'] is not None else None,
                'status': item['status'] if item['status'] is not None else None,
                'status_display_name': item['statusDisplayName'] if item['statusDisplayName'] is not None else None,
                'ruling_date': item['rulingDate'] if item['rulingDate'] is not None else None,
                'hearing_date': item['hearingDate'] if item['hearingDate'] is not None else None,
                'date_entered': item['dateEntered'] if item['dateEntered'] is not None else None,
            }
            per_id = self.env['ks.hisa.ruling.persons.involved'].create(pers_to_create)
            persons_ids.append(per_id.id)
        return persons_ids

    def get_persons_installments(self, data):
        installments_ids = []
        for item in data:
            installments_to_create = {
                'installments_amount': item['amount'],
                'installments_due_date': datetime.datetime.strptime(item['dueDate'], "%Y-%m-%d").date(),
            }
            inst_id = self.env['ks.hisa.installments'].create(installments_to_create)
            installments_ids.append(inst_id.id)
        return installments_ids

    def get_persons_suspension(self, data):
        suspension_ids = []
        for item in data:
            suspension_to_create = {
                'suspension_dates': item,
            }
            suspen_id = self.env['ks.hisa.suspension'].create(suspension_to_create)
            suspension_ids.append(suspen_id.id)
        return suspension_ids

    def get_horses_involved(self, data):
        horses_ids = []
        for item in data:
            horses_involved_to_create = {
                'hisa_horse_id': item['hisaHorseId'] if item['hisaHorseId'] is not None else None,
                'horse_name': item['horseName'] if item['horseName'] is not None else None,
                'suspension_start': item['suspension']['start'] if item['suspension'] is not None and
                                                                   item['suspension']['start'] is not None else None,
                'suspension_duration': item['suspension']['duration'] if item['suspension'] is not None and
                                                                         item['suspension'][
                                                                             'duration'] is not None else None,
                'suspension_dates_ids': [(6, 0, self.get_horses_suspension(item['suspension']['dates']))] if item[
                                                                                                                 'suspension'] is not None and
                                                                                                             item[
                                                                                                                 'suspension'][
                                                                                                                 'dates'] is not None else None,
                'barred_from_racing': item['barredFromRacing'] if item['barredFromRacing'] is not None else None,
            }
            horses_id = self.env['ks.hisa.horses.involved'].create(horses_involved_to_create)
            horses_ids.append(horses_id.id)
        return horses_ids

    def get_horses_suspension(self, data):
        suspension_ids = []
        for item in data:
            suspension_to_create = {
                'suspension_dates': item,
            }
            suspen_id = self.env['ks.hisa.horses.suspension'].create(suspension_to_create)
            suspension_ids.append(suspen_id.id)
        return suspension_ids
