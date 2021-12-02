#!/usr/bin/env bash

export PGSERVICE=sylvis_import

DIR=$(git rev-parse --show-toplevel)

mkdir -p ${DIR}/src/sylvis/fixtures

for i in {2..5}; do
  psql --tuples-only -c "select json_agg(row_to_json(r))
  from (
  	select 'sylvis.sector' as model,
  	('00000000-1111-000${i}-0000-000000' || lpad(id::text, 6, '0'))::uuid as pk,
  	jsonb(row_to_json(t))-'id' as fields
  	from (select id, name,
          $( (( $i < 5 )) && echo "('00000000-1111-000$((i+1))-0000-000000' || lpad(niv$((i+1))_id::text, 6, '0'))::uuid as parent," || echo "")
  		    coalesce(descr, '') as description
  		  from parzellen.niv${i}) t
  ) r" > ${DIR}/src/sylvis/fixtures/sector${i}.json
done


psql --tuples-only -c "select json_agg(row_to_json(r))
from (
	select 'sylvis.plot' as model,
	('00000000-1111-0001-0000-000000' || lpad(id::text, 6, '0'))::uuid as pk,
	jsonb(row_to_json(t))-'id' as fields
	from (select id, name,
  		  accr_an as yearly_growth,
  		  etale,
  		  an_nxt_coupe as planned_next_section,
  		  an_nxt_soins as planned_next_treatment,
  		  rotation_coupes as rotation_sections,
  		  rotation_soins as rotation_treatments,
  		  ('00000000-1111-0002-0000-000000' || lpad(niv2_id::text, 6, '0'))::uuid as sector,
  		  st_astext(geom) as geom
		  from parzellen.div) t
) r" > ${DIR}/src/sylvis/fixtures/plots.json
