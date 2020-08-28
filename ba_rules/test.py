from durable.lang import *
import sys
import random
import uuid
import time



clients_charges = {
    "CL1": [
        {
            "name": "OWP",
            "charge": 120,
            "variable": "fixed",
            "variable_attr": None,
            "rules": [
                {"predicate": "length", "operator": "$gt", "value": 100}
            ]
        },
        {
            "name": "OSP",
            "charge": 10,
            "variable": "per/kg",
            "variable_attr": "weight",
            "rules": [
                {"predicate": "weight", "operator": "$gt", "value": 25}
            ]
        }
    ],
    "CL2": [
        {
            "name": "OWP",
            "charge": 120,
            "variable": "fixed",
            "variable_attr": None,
            "rules": [
                {"predicate": "length", "operator": "$gt", "value": 50}
            ]
        },
        {
            "name": "OSP",
            "charge": 10,
            "variable_attr": "weight",
            "variable": "per/kg",
            "rules": [
                {"predicate": "weight", "operator": "$gt", "value": 25}
            ]
        }
    ]
}


def calculate_charge(shipment):
    charges_config = shipment.charge_config
    variable = charges_config.variable
    charge = charges_config.charge
    if variable == "per/kg":
        variable_attr = charges_config.variable_attr
        weight = getattr(shipment, variable_attr, 0)
        return weight * charge
    return charge


def owp_callback(c):
    """
    {'id': '5a4f1c30e587434188b80d1f2eacbbda', 'length': 71, 'weight': 10, 'charge_config': {'name': 'OWP', 'charge': 120, 'variable': 'fixed', 'variable_attr': None, 'rules': [{'predicate': 'length', 'operator': '$gt', 'value': 50}]}}
    """
    shipment = c.m
    shipment_id = shipment.id
    charges = calculate_charge(shipment)
    print(f'OWP Charges for shipment {shipment_id} is {charges}')


def osp_callback(c):
    shipment = c.m
    shipment_id = shipment.id
    charges = calculate_charge(shipment)
    print(f'OSP Charges for shipment {shipment_id} is {charges}')


class ShipmentGenerator(object):
    def __init__(self, client_name, count=10):
        self.client_name = client_name
        self.count = count

    def get_charges(self):
        return clients_charges.get(self.client_name)

    def get_weight(self):
        return random.randint(10, 100)

    def get_length(self):
        return random.randint(10, 200)

    def get_shipments(self):
        shipments = []
        for i in range(self.count):
            shipments.append(
                {
                    "id": uuid.uuid4().hex,
                    "length": self.get_length(),
                    "weight": self.get_weight()
                }
            )
        return shipments


class RulesFactory(object):
    def __init__(self):
        self.host = engine.Host()

    def get_callback(self, charge_name):
        return getattr(sys.modules[__name__], "%s_callback" % charge_name.lower())

    def get_lang(self, charge_name, rules):
        rules_lang = []
        for rule in rules:
            rules_lang.append({"m": {rule["operator"]: {rule["predicate"]: rule["value"]}}})
        callback = self.get_callback(charge_name)
        lang = {"run": callback, "all": rules_lang}
        return lang

    def add_charge_to_shipment(self, shipment_object, charge_config):
        shipment_object["charge_config"] = charge_config
        return shipment_object

    def register_rules(self, charges):
        for charge in charges:
            name = charge["name"]
            rules = charge["rules"]
            lang = self.get_lang(name, rules)
            ruleset = {name: {"r_0": lang}}
            self.host.set_rulesets(ruleset)

    def run_rule(self, shipment_object, charges):
        for charge in charges:
            charge_name = charge["name"]
            shipment_object = self.add_charge_to_shipment(shipment_object, charge)
            try:
                self.host.post(charge_name, shipment_object)
            except engine.MessageNotHandledException as e:
                print("No rule run - %s" % e)



if __name__ == "__main__":
    for _ in range(0, 10):
        client_name = random.choice(["CL1", "CL2"])
        print(f"Running rule for {client_name}")
        gen = ShipmentGenerator(client_name)
        charges = gen.get_charges()
        shipments = gen.get_shipments()
        f = RulesFactory()
        f.register_rules(charges)
        for shipment in shipments:
            f.run_rule(shipment, charges)
        print("sleeping now")
        time.sleep(1)
