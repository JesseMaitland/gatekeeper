CREATE GROUP {{groups.name}};

-- granting usage access to {{groups.name}}
{% for schema in groups.schemas%}
GRANT USAGE ON SCHEMA {{schema}} TO GROUP {{groups.name}};
{%endfor%}


-- granting read / write access to {{groups.name}}
{% for schema in groups.schemas%}
{%if groups.permissions[0] == 'all' %}GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA {{schema}} TO GROUP {{groups.name}};
{%else%}
GRANT {%for p in groups.permissions%}{{p.upper()}}{% if not loop.last %}, {% endif %}{%endfor%} ON ALL TABLES IN SCHEMA {{schema}} TO GROUP {{groups.name}};
{%endif%}
{%endfor%}
