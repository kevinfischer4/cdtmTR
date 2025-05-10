from database_handler import add_friend
from database_handler import connect_to_database, close_connection, insert_portfolio


if __name__ == "__main__":
    cur, conn = connect_to_database()
    if cur and conn:
        add_friend(cur, "31ed74cb-c2d3-4cac-995e-51f935490639", "5d267630-b154-40f9-80bd-227bf66c7963")
        conn.commit()
        
    close_connection(cur, conn)
        
        
        