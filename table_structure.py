# orders.pkl
orders_data = {
    'orders': {
        'ORD1001': {  # Order对象的序列化数据
            'order': Order(),
            'customer_id': 'P1000',
            'status': 'paid',  # paid/fulfilled/cancelled
            'items': [...],
            'order_amount': Decimal('100.00'),
            'delivery_fee': Decimal('10.00'),
            'total_amount': Decimal('110.00')
        }
    },
    'indices': {
        'by_status': {
            'paid': ['ORD1001'],
            'fulfilled': ['ORD1002'],
            'cancelled': ['ORD1003']
        },
        'by_date': {
            '2024': {
                '04': ['ORD1001', 'ORD1002']
            }
        },
        'by_customer': {
            'P1000': ['ORD1001']
        }
    }
}

# payments.pkl
payments_data = {
    'payments': {
        'PAY1001': {
            'payment': Payment(),  # Payment对象
            'order_id': 'ORD1001',
            'customer_id': 'P1000'
        }
    },
    'indices': {
        'by_order': {
            'ORD1001': ['PAY1001']
        },
        'by_customer': {
            'P1000': ['PAY1001']
        },
        'by_date': {
            '2024': {
                '04': ['PAY1001']
            }
        }
    }
}

# sales.pkl
sales_data = {
    'sales_summary': {
        'weekly': {
            '2024-W17': {
                'current': {
                    'order_count': 0,
                    'total_amount': Decimal('0.00')
                },
                'previous': {
                    'fulfilled': {
                        'order_count': 0,
                        'total_amount': Decimal('0.00')
                    },
                    'cancelled': {
                        'order_count': 0,
                        'total_amount': Decimal('0.00')
                    }
                }
            }
        },
        'monthly': {...},
        'yearly': {...}
    },
    'popular_items': {
        'weekly': {
            '2024-W17': {
                'current': {},
                'previous': {}
            }
        },
        'monthly': {...},
        'yearly': {...}
    }
}


##新增的

# orders.pkl
orders_data = {
    'orders': {
        'ORD1001': {  # Order对象的序列化数据
            'order': Order(),
            'customer_id': 'P1000',
            'status': 'paid',  # paid/fulfilled/cancelled
            'items': [...],
            'order_amount': Decimal('100.00'),
            'delivery_fee': Decimal('10.00'),
            'total_amount': Decimal('110.00')
        }
    },
    'indices': {
        'by_status': {
            'paid': ['ORD1001'],
            'fulfilled': ['ORD1002'],
            'cancelled': ['ORD1003']
        },
        'by_date': {
            '2024': {
                '04': ['ORD1001', 'ORD1002']
            }
        },
        'by_customer': {
            'P1000': ['ORD1001']
        }
    }
}

# payments.pkl
payments_data = {
    'payments': {
        'PAY1001': {
            'payment': Payment(),  # Payment对象
            'order_id': 'ORD1001',
            'customer_id': 'P1000'
        }
    },
    'indices': {
        'by_order': {
            'ORD1001': ['PAY1001']
        },
        'by_customer': {
            'P1000': ['PAY1001']
        },
        'by_date': {
            '2024': {
                '04': ['PAY1001']
            }
        }
    }
}

# sales.pkl
sales_data = {
    'sales_summary': {
        'weekly': {
            '2024-W17': {
                'current': {
                    'order_count': 0,
                    'total_amount': Decimal('0.00')
                },
                'previous': {
                    'fulfilled': {
                        'order_count': 0,
                        'total_amount': Decimal('0.00')
                    },
                    'cancelled': {
                        'order_count': 0,
                        'total_amount': Decimal('0.00')
                    }
                }
            }
        },
        'monthly': {...},
        'yearly': {...}
    },
    'popular_items': {
        'weekly': {
            '2024-W17': {
                'current': {},
                'previous': {}
            }
        },
        'monthly': {...},
        'yearly': {...}
    }
}