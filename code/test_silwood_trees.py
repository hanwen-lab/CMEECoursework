from clean_silwood_trees import validate_record, process_records, summarise_oaks


valid_row = {
    "record_id": "ST901",
    "location": "Manor House",
    "genus": "Quercus",
    "species": "robur",
    "distance_m": "10",
    "angle_degrees": "45",
}

clean_record, reasons = validate_record(valid_row, 2, set())
assert reasons == []
assert clean_record is not None

text_row = valid_row.copy()
text_row["location"] = "  mAnOr HoUsE  "
clean_record, reasons = validate_record(text_row, 2, set())
assert reasons == []
assert clean_record["location"] == "Manor House"

missing_row = valid_row.copy()
missing_row["location"] = "   "
clean_record, reasons = validate_record(missing_row, 2, set())
assert clean_record is None
assert reasons == ["missing location"]

unknown_row = valid_row.copy()
unknown_row["location"] = "Unknown Site"
clean_record, reasons = validate_record(unknown_row, 2, set())
assert clean_record is None
assert reasons == ["invalid location"]

boundary_row = valid_row.copy()
boundary_row["distance_m"] = "100"
clean_record, reasons = validate_record(boundary_row, 2, set())
assert clean_record is not None
assert reasons == []

zero_row = valid_row.copy()
zero_row["distance_m"] = "0"
clean_record, reasons = validate_record(zero_row, 2, set())
assert clean_record is None
assert reasons == ["distance_m out of range"]

invalid_number_row = valid_row.copy()
invalid_number_row["distance_m"] = "ten"
clean_record, reasons = validate_record(invalid_number_row, 2, set())
assert clean_record is None
assert reasons == ["invalid distance_m"]

nan_row = valid_row.copy()
nan_row["distance_m"] = "NaN"
clean_record, reasons = validate_record(nan_row, 2, set())
assert clean_record is None
assert reasons == ["invalid distance_m"]

inf_row = valid_row.copy()
inf_row["distance_m"] = "inf"
clean_record, reasons = validate_record(inf_row, 2, set())
assert clean_record is None
assert reasons == ["invalid distance_m"]

angle_row = valid_row.copy()
angle_row["angle_degrees"] = "90"
clean_record, reasons = validate_record(angle_row, 2, set())
assert clean_record is None
assert reasons == ["angle_degrees out of range"]

valid_angle_row = valid_row.copy()
valid_angle_row["angle_degrees"] = "0.1"
clean_record, reasons = validate_record(valid_angle_row, 2, set())
assert clean_record is not None
assert reasons == []

clean_record, reasons = validate_record(valid_row, 2, {"ST901"})
assert clean_record is None
assert reasons == ["duplicate record_id"]

id_row = valid_row.copy()
id_row["record_id"] = "st901"
clean_record, reasons = validate_record(id_row, 2, set())
assert clean_record is None
assert reasons == ["invalid record_id"]

multi_row = valid_row.copy()
multi_row["location"] = ""
multi_row["distance_m"] = "0"
clean_record, reasons = validate_record(multi_row, 2, set())
assert clean_record is None
assert reasons == ["missing location", "distance_m out of range"]

pair_row = valid_row.copy()
pair_row["species"] = "excelsior"
clean_record, reasons = validate_record(pair_row, 2, set())
assert clean_record is None
assert reasons == ["invalid genus/species combination"]

genus_row = valid_row.copy()
genus_row["genus"] = "Quercuss"
clean_record, reasons = validate_record(genus_row, 2, set())
assert clean_record is None
assert reasons == ["invalid genus"]

accepted, issues = process_records([invalid_number_row, valid_row])
assert len(accepted) == 1
assert len(issues) == 1
assert accepted[0]["record_id"] == "ST901"
assert issues[0]["source_row"] == "2"
assert issues[0]["reasons"] == "invalid distance_m"

duplicate_rows = [valid_row, valid_row.copy()]
accepted, issues = process_records(duplicate_rows)
assert len(accepted) == 1
assert len(issues) == 1
assert "duplicate record_id" in issues[0]["reasons"]

earlier_row = valid_row.copy()
earlier_row["record_id"] = "ST900"
accepted, issues = process_records([valid_row, earlier_row])
assert [row["record_id"] for row in accepted] == ["ST900", "ST901"]

oak_rows = [
    {"genus": "Quercus", "species": "robur"},
    {"genus": "Quercus", "species": "robur"},
    {"genus": "Quercus", "species": "petraea"},
    {"genus": "Quercuss", "species": "robur"},
]
oak_counts = summarise_oaks(oak_rows)
assert oak_counts == [
    {"species": "petraea", "count": "1"},
    {"species": "robur", "count": "2"},
]

non_oak_rows = [{"genus": "Acer", "species": "pseudoplatanus"}]
assert summarise_oaks(non_oak_rows) == []

print("OK.")
