import logging

from odoo import models, fields

_logger = logging.getLogger()


class KeyHisausappsRuling(models.Model):
    _name = 'ks.hisa.ruling'
    _description = 'Ks Hisa Ruling'

    hisa_ruling_id = fields.Char(string='Hisa Ruling ID', )
    action_code = fields.Char()
    customCode = fields.Char()
    location_id = fields.Char(string='location ID', )
    date_ruling = fields.Date()
    persons_involved_ids = fields.Many2many(comodel_name='ks.hisa.ruling.persons.involved', )
    # files_uri_ids = fields.One2many(comodel_name='ks.hisa.files.uri', inverse_name='hisa_ruling_id')


class KeyHisausappsRulingPersonsInvolved(models.Model):
    _name = 'ks.hisa.ruling.persons.involved'
    _description = 'ks.hisa.ruling.persons.involved'

    hisa_person_id = fields.Char(string='Hisa Ruling ID')
    person_name = fields.Char()

    fine_amount = fields.Float()
    fine_recovery_amount = fields.Integer()
    fine_recovery_date = fields.Date()
    fine_paid = fields.Boolean()
    fine_total = fields.Integer()
    fine_amount_paid = fields.Integer()
    fine_payment_due = fields.Date()
    fine_installments_ids = fields.Many2many(comodel_name='ks.hisa.installments')
    #не добавленно
    # suspension_start = fields.Date()
    # suspension_duration = fields.Integer()
    # suspension_dates = fields.Date()
    #
    # points_amount = fields.Integer()
    # points_expireDate = fields.Date()
    # points_duration = fields.Integer()




class RulingFineInstallments(models.Model):
    _name = 'ks.hisa.installments'
    _description = 'ks.hisa.installments'

    installments_amount = fields.Integer()
    installments_due_date = fields.Date()


# class RulingFiles(models.Model):
#     _name = 'ks.hisa.files.uri'
#     _inherit = 'ir.attachment'
#
#     hisa_ruling_id = fields.Many2one(comodel_name='ks.hisa.ruling')






    # {
    #     "hisaRulingId": "R000000001",
    #     "actionCode": "2022-00001",
    #     "customCode": null,
    #     "locationId": "L000000035",
    #     "date": "2022-07-20",
    #     "personsInvolved": [
    #         {
    #             "hisaPersonId": "P000000023",
    #             "personName": "Dmytro Berbeka",
    #             "fine": {
    #                 "amount": 250,
    #                 "costRecovery": {
    #                     "amount": 500,
    #                     "dueDate": "2023-03-24"
    #                 },
    #                 "paid": false,
    #                 "total": 750,
    #                 "amountPaid": 375,
    #                 "paymentDue": "2023-04-21",
    #                 "installments": [
    #                     {
    #                         "amount": 375,
    #                         "dueDate": "2023-03-22"
    #                     },
    #                     {
    #                         "amount": 375,
    #                         "dueDate": "2023-04-21"
    #                     }
    #                 ]
    #             },
    #             "suspension": null,
    #             "points": null,
    #             "purseForfeiturePercent": {
    #                 "amount": 777,
    #                 "paid": false,
    #                 "disqualified": false,
    #                 "withheld": false
    #             },
    #             "requiredActions": {
    #                 "description": null,
    #                 "completed": false,
    #                 "completeByDate": "2023-02-18",
    #                 "finePerCalendarDay": 0
    #             },
    #             "details": {
    #                 "regulationNumber": "2272 (a)",
    #                 "description": "The use of Shock Wave Therapy shall be disclosed to the Regulatory Veterinarian no less than 48 hours prior to use and shall not be permitted",
    #                 "stewardsRuling": null,
    #                 "rscRuling": "Testing Racetrack Safety Committee Decision",
    #                 "nspRuling": "Testing Internal adjudication panel decision",
    #                 "arbitralRuling": "Testing Arbitral body decision",
    #                 "hisaBoardApealRuling": "Testing hisa board appeal decision",
    #                 "boardPanelRuling": "Testing board panel",
    #                 "hisaBoardRuling": "Testing hisa board decision"
    #             },
    #             "status": "RulingIssued",
    #             "statusDisplayName": "Ruling Issued",
    #             "rulingDate": "2023-01-19",
    #             "hearingDate": null,
    #             "dateEntered": "2023-01-19"
    #         },
    #         {
    #             "hisaPersonId": "P000030206",
    #             "personName": "Neil Vet1 Caretaker",
    #             "fine": {
    #                 "amount": 1000,
    #                 "costRecovery": null,
    #                 "paid": true,
    #                 "total": 0,
    #                 "amountPaid": 0,
    #                 "paymentDue": "2024-03-31",
    #                 "installments": null
    #             },
    #             "suspension": null,
    #             "points": {
    #                 "amount": 200,
    #                 "expireDate": "2024-02-17",
    #                 "duration": 365
    #             },
    #             "purseForfeiturePercent": {
    #                 "amount": 1000,
    #                 "paid": true,
    #                 "disqualified": false,
    #                 "withheld": false
    #             },
    #             "requiredActions": null,
    #             "details": {
    #                 "regulationNumber": "1234",
    #                 "description": "Test",
    #                 "stewardsRuling": "Test",
    #                 "rscRuling": null,
    #                 "nspRuling": null,
    #                 "arbitralRuling": null,
    #                 "hisaBoardApealRuling": null,
    #                 "boardPanelRuling": null,
    #                 "hisaBoardRuling": null
    #             },
    #             "status": "RulingIssued",
    #             "statusDisplayName": "Ruling Issued",
    #             "rulingDate": "2023-02-17",
    #             "hearingDate": "2023-02-28",
    #             "dateEntered": "2023-02-17"
    #         }
    #     ],
    #     "horsesInvolved": [
    #         {
    #             "hisaHorseId": "H000027813",
    #             "horseName": "Far's Last One",
    #             "suspension": {
    #                 "start": null,
    #                 "duration": null,
    #                 "dates": [
    #                     "2023-03-23",
    #                     "2023-04-22"
    #                 ]
    #             },
    #             "barredFromRacing": false
    #         },
    #         {
    #             "hisaHorseId": "H000032418",
    #             "horseName": "Chasin Gracie",
    #             "suspension": {
    #                 "start": "2023-04-10",
    #                 "duration": 19,
    #                 "dates": null
    #             },
    #             "barredFromRacing": false
    #         }
    #     ],
    #     "adjudicatorsHisaId": {
    #         "hisaBoard": null,
    #         "boardPanel": null,
    #         "arbitralPanel": null,
    #         "rscMembers": null,
    #         "nspMembers": null,
    #         "trackStewards": [
    #             "P999999992"
    #         ]
    #     },
    #     "filesUri": [
    #         "R000000001/ruling/16cac719-33b0-4935-8384-c286ef18427b.png",
    #         "R000000001/ruling/2253908e-6de3-4573-a155-b8cac7157287.pdf",
    #         "R000000001/ruling/70c0fdfe-a8b9-4ad4-a9aa-8a13f13c82b8.pdf",
    #         "R000000001/ruling/73912af5-a84a-43c4-a752-d616a64410cd.png",
    #         "R000000001/ruling/8ffe6f6f-df1c-4786-9875-a99ded278558.png",
    #         "R000000001/ruling/e7761759-4db4-41c0-949a-a31d92dbb480.pdf",
    #         "R000000001/ruling/f756e53f-2fe4-4232-99f1-a3e9541e119a.png"
    #     ],
    #     "status": "RulingIssued",
    #     "stage": "BoardPanel",
    #     "rulingBody": "HISA",
    #     "canBeAppealed": false,
    #     "rulingDate": "2023-01-19",
    #     "dateEntered": "2023-01-19",
    #     "lastDayOfAppeal": "2023-01-30",
    #     "horseId": "H999998978",
    #     "raceNumber": "1",
    #     "responsiblePersonHisaId": null,
    #     "ownerHisaId": null,
    #     "classification": "Crop",
    #     "locationName": "Belmont Park",
    #     "horseName": "Flash of Mischief",
    #     "responsiblePersonName": "",
    #     "ownerName": "",
    #     "statusDisplayName": "Ruling Issued",
    #     "reportingDate": "2023-03-17"
    # },
