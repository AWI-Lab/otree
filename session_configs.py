SESSION_CONFIGS = [
    {
        'name': 'public_goods',
        'display_name': "Public Goods",
        'num_demo_participants': 6,
        'app_sequence': ['public_goods', 'payment_info'],
    },
    {
        'name': 'public_goodsMartin',
        'display_name': "Martins Public Goods",
        'num_demo_participants': 15,
        'app_sequence': ['public_goodsMartin', 'payment_info'],
    },
    {
        'name': 'active_passive_demo',
        'display_name': 'DEMO Active / Passive Risk Taking - 1 Round',
        'app_sequence': [
            'risktaking_instructions', 
            'risktaking', 
            'risktaking_lastpart'
        ],
        'num_demo_participants': 4,
        'real_world_currency_per_point': 0.02,
        'participation_fee': 3.00,
        'main_task_rounds': 1
    },
    {
        'name': 'active_passive',
        'display_name': 'Active / Passive Risk Taking - 10 Rounds',
        'app_sequence': [
            'risktaking_instructions', 
            'risktaking', 
            'risktaking_lastpart'
        ],
        'num_demo_participants': 4,
        'real_world_currency_per_point': 0.02,
        'participation_fee': 3.00,
        'main_task_rounds': 10
    },
    {
        'name': 'single_fixed',
        'display_name': "RiskOther - SINGLE Fixed",
        'num_demo_participants': 2,
        'participation_fee': 3.00,
        'app_sequence': ['single'],
        'compensation': 'fixed',     # Enter either fixed, variable_result or variable_profit
    },
    {
        'name': 'single_result',
        'display_name': "RiskOther - SINGLE Variable Result",
        'num_demo_participants': 2,
        'participation_fee': 3.00,
        'app_sequence': ['single'],
        'compensation': 'variable_result',     # Enter either fixed, variable_result or variable_profit
    },
    {
        'name': 'single_profit',
        'display_name': "RiskOther - SINGLE Variable Profit",
        'num_demo_participants': 2,
        'participation_fee': 3.00,
        'app_sequence': ['single'],
        'compensation': 'variable_profit',     # Enter either fixed, variable_result or variable_profit
    },
    {
        'name': 'group_fixed',
        'display_name': "RiskOther - GROUP Treatment Fix",
        'num_demo_participants': 6,
        'participation_fee': 3.00,
        'app_sequence': ['group'],
        'compensation': 'fixed',     # Enter either fixed, variable_result or variable_profit

    },
    {
        'name': 'group_result',
        'display_name': "RiskOther - GROUP Treatment Variable Result",
        'num_demo_participants': 6,
        'participation_fee': 3.00,
        'app_sequence': ['group'],
        'compensation': 'variable_result',     # Enter either fixed, variable_result or variable_profit

    },
    {
        'name': 'group_profit',
        'display_name': "RiskOther - GROUP Treatment Variable Profit",
        'num_demo_participants': 6,
        'participation_fee': 3.00,
        'app_sequence': ['group'],
        'compensation': 'variable_profit',     # Enter either fixed, variable_result or variable_profit

    }
]
