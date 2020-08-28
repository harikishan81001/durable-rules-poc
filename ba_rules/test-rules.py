from durable.lang import *



class FreightChargeRuleEvaluator(object):
    def __init__(self, freight_order, shipment_details):
        self.freight_order = freight_order
        self.shipment_details = shipment_details
    DEFINED_OPERATOR = {
    }
    @staticmethod
    def shipment_rule_evaulate(rule):
        # get object value from data
        # replace object value in rule
        # evaluate rule
        pass
"""
rule1: if length > 120cm, apply OSP charge
rule2: if length > 100cm, do volumetric weight
"""
osp = 100
with ruleset('osp'):
    @when_all(s.length > 120)
    def side_validation(c):
        print('executing rule')
        c.s.charge += osp


[
    {
        "object": "length",
        "operator": "<",
        "value": "1000"
    }
]


class Shipment(object):
    length = 101
    width = 104
    charges = {}


class R(object):
    def get_charge(shipment):
        return 1000

    object = "length"
    operator = "<"
    value = "1000"


"""
with ruleset('osp'):
    @when_all(m.length < 1000 && m.width > 1000)
    def side_validation(c):
        print('executing rule')
        c.m.charges["OSP"] = R.get_charge(c.m)

"""

update_state('osp', Shipment)
update_state('osp', {'length': 121})