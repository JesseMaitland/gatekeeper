def execute_query(self, query: str, params: List = None, fetch: bool = True) -> Tuple:
    with self.redshift_connection() as conn:
        with conn.cursor() as cursor:
            result = None

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            if fetch:
                result = cursor.fetchall()

            conn.commit()
            return result
