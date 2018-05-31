from logger.log_db_adapter import LogDBAdapter


if __name__ == '__main__':
    db_path = '../db/ai_api.db'
    sql_debug = False
    db_adapter = LogDBAdapter(
        db_path=db_path,
        create_tables=True,
        sql_debug=sql_debug
    )
    db_adapter.show_log()
