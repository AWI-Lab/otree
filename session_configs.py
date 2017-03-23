SESSION_CONFIGS = [
    {
        'name': 'public_goods',
        'display_name': "Public Goods",
        'num_demo_participants': 3,
        'app_sequence': ['public_goods', 'payment_info'],
    },
    {
        'name': 'active_passive',
        'display_name': 'Active / Passive Risk Taking',
        'app_sequence': ['risktaking_instructions', 'risktaking', 'risktaking_lastpart'],
        'num_demo_participants': 2,
        'real_world_currency_per_point': 0.02,
        'participation_fee': 3.00,
        'main_task_rounds': 10
    }
]
