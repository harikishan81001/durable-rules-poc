from durable.lang import *
from durable.engine import Ruleset, Host


# class RulesFactory(object):
#     def get_rule(self, value):
#         with ruleset('test'):
#             return when_all(m.subject == value)

# # r = RulesFactory().get_rule("")



# # obj = eval(r)

# rs = ruleset("test")
# cond = when_all(m.subject == 'World')
# rs.rules = cond




def say_hello(c):
    print ('Hello {0}'.format(c.m.subject))




# # data = {'r_0': {'all': [{'m': {'subject': 'World'}}], 'run': say_hello}}
# # rule_name = "test"
# # _main_host = Host()

# # rs = Ruleset(rule_name, _main_host, data)


# with ruleset('test'):
#     @when_all(m.subject == 'World')
#     def say_hello(c):
#         print ('Hello {0}'.format(c.m.subject))

# import pdb; pdb.set_trace()

# post('test', { 'subject': 'World' })


# # #####################################
# # def apply_deco(deco_name, value):
# #     print(f'applying {deco_name}')
# #     if deco_name == "match_subject":
# #         with ruleset('test'):
# #             return when_all(m.subject == value)

# #     print('nothing to apply')
# #     return

# # @apply_deco("match_subject", "world")
# # def say_hello(c):
# #     print ('Hello {0}'.format(c.m.subject))
# # #######################################

# # RulesFactory().get_rule("world")





# # _rulesets["test"].__dict__["rules"][0].__dict__["expression"][0].__dict__



from durable.lang import *

def callback(c):
    print(c.__dict__)
    print('risk7 fraud detected')

get_host().set_rulesets({ 'test': {
    'suspect': {
        'run': callback,
        'all': [
            {'m': {
                "$gt": {'amount': 100
                }
            }
        },
        ],
    }
}})



post('test', { 'amount': 99 })


# post('risk7', {'t': 'purchase', 'location': 'US'})
# post('risk7', {'t': 'purchase', 'location': 'CA'})