from sqlalchemy.dialects.postgresql import insert


def upsert(session, model, match_columns: list[str], values: dict):
    """
    Generic upsert helper using PostgreSQL ON CONFLICT.
    match_columns = columns defining uniqueness.
    """
    stmt = insert(model).values(values)
    stmt = stmt.on_conflict_do_update(
        index_elements=match_columns, set_={k: stmt.excluded[k] for k in values.keys()}
    )
    session.execute(stmt)

    # Query the record back to return the instance
    return (
        session.query(model)
        .filter(*(getattr(model, c) == values[c] for c in match_columns))
        .one()
    )
