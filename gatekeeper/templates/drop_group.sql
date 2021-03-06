/*************************************************************************
  This file generated by gatekeeper, the redshift permissions management tool
    group name: {{groups}}
**************************************************************************/



-- revoke all access from all objects in the database.
{% for schema in schemas %}
-- remove access for {{schema.name}} / {{users}}
REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA {{schema.name}} FROM GROUP {{groups}};
REVOKE ALL PRIVILEGES ON ALL ROUTINES IN SCHEMA {{schema.name}} FROM GROUP {{groups}};

{%endfor%}

{% for user in db_users%}
ALTER GROUP {{groups}} DROP USER {{user.name}};
{%endfor%}

DROP GROUP {{groups}};

