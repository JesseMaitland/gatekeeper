from argparse import Namespace
from typing import Dict
from cryptography.fernet import Fernet
from jinja2 import Template
from gatekeeper.src.environment import gatekeeper_env, get_jinja_environment
from gatekeeper.src.configparsing import GateKeeper, User
from gatekeeper.src.paths import CONFIG_FILE, PLANNED_USERS_DIR, USER_INDEX_FILE, GATEKEEPER_SECRETS, INDEX_DIR, \
    PASSWORD_INDEX_FILE
from gatekeeper.src.index import hash_file, read_index, save_index
from gatekeeper.src.password import generate_password, get_fernet, create_md5_password_hash, encrypt_password


def users(cmd: Namespace) -> None:
    # set up a gatekeeper
    gatekeeper = GateKeeper.from_configs(CONFIG_FILE)

    # get the jinja template for the users
    template = get_jinja_environment().get_template('user.sql')

    # get the indexes
    user_index = read_index(USER_INDEX_FILE)
    password_index = read_index(PASSWORD_INDEX_FILE)

    # just assume we will need a fernet key
    fernet = get_fernet(GATEKEEPER_SECRETS)

    # figure out what we are doing for each user
    for user in gatekeeper.users.values():

        # if the user does not exist in the index, they are to be added, so we need
        # to generate a password, and new file for them
        if user.name not in user_index.keys():
            # generate a password for the new user.
            password = generate_password()
            md5_password_hash = create_md5_password_hash(user.name, password)
            encrypted_password = encrypt_password(password, fernet)

            # render the user file, and hash what we have created.
            user_sql_file_content = template.render(user=user)
            user_sql_file_content_md5_hash = hash_file(user_sql_file_content)

            # set the password, and the user hash in the indexes
            user_index[user.name] = user_sql_file_content_md5_hash

            # update the password index
            password_index[user.name] = {}
            password_index[user.name]['md5'] = md5_password_hash
            password_index[user.name]['encrypted'] = encrypted_password

            # save the user file
            file_path = PLANNED_USERS_DIR / user.file_name
            file_path.touch(exist_ok=True)
            file_path.write_text(user_sql_file_content)

            # that is all we are doing for this user, so get the next one
            continue

        if user.name in user_index.keys():  # this is an existing user, do update, update password if set

            # render the template
            user_sql_file_content = template.render(user=user)
            user_sql_file_content_md5_hash = hash_file(user_sql_file_content)

            user_index[user.name] = user_sql_file_content_md5_hash

            # save the user file
            file_path = PLANNED_USERS_DIR / user.file_name
            file_path.touch(exist_ok=True)
            file_path.write_text(user_sql_file_content)

            # if we are cycling the passwords, do that now
            if cmd.rotate_passwords:
                password = generate_password()
                md5_password_hash = create_md5_password_hash(user.name, password)
                encrypted_password = encrypt_password(password, fernet)

                # update the password
                password_index[user.name] = {}
                password_index[user.name]['md5'] = md5_password_hash
                password_index[user.name]['encrypted'] = encrypted_password

    # always update the indexes
    save_index(USER_INDEX_FILE, user_index)
    save_index(PASSWORD_INDEX_FILE, password_index)


def groups(cmd: Namespace) -> None:
    print('groups')


def plan(cmd: Namespace) -> None:
    print('plan')
