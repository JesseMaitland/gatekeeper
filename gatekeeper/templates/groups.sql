CREATE GROUP {{group.name}};

-- granting usage access to {{group.name}}
{% for schema in group.schemas%}
GRANT USAGE ON SCHEMA {{schema}} TO GROUP {{group.name}};
{%endfor%}


-- granting read / write access to {{group.name}}
{% for schema in group.schemas%}
{%if group.permissions[0] == 'all' %}GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA {{schema}} TO GROUP {{group.name}};
{%else%}
GRANT {%for p in group.permissions%}{{p.upper()}}{% if not loop.last %}, {% endif %}{%endfor%} ON ALL TABLES IN SCHEMA {{schema}} TO GROUP {{group.name}};
{%endif%}
{%endfor%}
