from inspect import signature


class BadFilterFormat(Exception):
    pass


class FilterMixin:

    operators = {
        '==': lambda f, a: f == a,
        'eq': lambda f, a: f == a,
        '!=': lambda f, a: f != a,
        'ne': lambda f, a: f != a,
        '>': lambda f, a: f > a,
        'gt': lambda f, a: f > a,
        '<': lambda f, a: f < a,
        'lt': lambda f, a: f < a,
        '>=': lambda f, a: f >= a,
        'ge': lambda f, a: f >= a,
        '<=': lambda f, a: f <= a,
        'le': lambda f, a: f <= a,
        'in': lambda f, a: f.in_(a),
        'not_in': lambda f, a: ~f.in_(a),
        'is_null': lambda f: f.is_(None),
        'is_not_null': lambda f: f.isnot(None),
    }

    @classmethod
    def _build_filters(cls, model, filters):
        sql_alchemy_filters = []
        for f in filters:
            field = f.get('field')
            op = f.get('op')
            value = f.get('val')

            if 'field' not in f.keys() and 'op' not in f.keys():
                raise BadFilterFormat('Invalid filter format. '
                                      '`field`, `op` parameters is required!')
            if op not in cls.operators:
                raise BadFilterFormat('Invalid filter operator!')

            op_function = cls.operators[op]
            arity = len(signature(op_function).parameters)
            sql_alchemy_field = getattr(model, field)
            sql_alchemy_filter = (op_function(sql_alchemy_field, value)
                                  if arity == 2 else op_function(sql_alchemy_field))
            sql_alchemy_filters.append(sql_alchemy_filter)

        return sql_alchemy_filters

    @classmethod
    def apply_filters(cls, query, model, filters):
        if not filters:
            return query

        sql_alchemy_filters = cls._build_filters(model, filters)
        if sql_alchemy_filters:
            query = query.filter(*sql_alchemy_filters)

        return query
