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
]
