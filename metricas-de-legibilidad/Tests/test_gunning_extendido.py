from model.PenalizacionPorComa import PenalizacionPorComa


casosPrueba = [
    {
        "nombre": "Financiamiento regional",
        "penalizacion": PenalizacionPorComa.MINIMUM,
        "sin_aposiciones": """
            The committee reviewed the regional funding proposal and approved a preliminary schedule for implementation.
            The report described budget constraints and administrative delays and expected benefits for local institutions.
            Several members asked for clearer deadlines and stronger monitoring and a public summary for citizens.
            The final decision kept the original objective and required each department to submit progress information every month.
            """,
        "con_aposiciones": """
            The committee, during a long meeting, reviewed the regional funding proposal and approved a preliminary schedule for implementation.
            The report, which described budget constraints and administrative delays and expected benefits for local institutions, guided the discussion.
            Several members, asking for clearer deadlines and stronger monitoring and a public summary for citizens, supported the plan.
            The final decision, keeping the original objective, required each department to submit progress information every month.
            """
    },
    {
        "nombre": "Contrato legal",
        "penalizacion": PenalizacionPorComa.HIGH,
        "sin_aposiciones": """
            The lessor grants the lessee the right to occupy the premises for residential purposes only.
            The lessee shall pay the monthly rent on the first day of each calendar month without deduction.
            Any modifications to the property require prior written consent from the lessor and must comply with applicable regulations.
            The agreement shall be governed by the laws of the jurisdiction where the property is located.
            """,
        "con_aposiciones": """
            The lessor, being the sole owner of record, grants the lessee, a natural person of legal age, the right to occupy the premises for residential purposes only.
            The lessee shall pay the monthly rent, currently fixed at the agreed amount, on the first day of each calendar month without deduction.
            Any modifications to the property, including structural changes and installations, require prior written consent from the lessor and must comply with applicable regulations.
            The agreement, entered into freely by both parties, shall be governed by the laws of the jurisdiction where the property is located.
            """
    },
    {
        "nombre": "Nota periodistica",
        "penalizacion": PenalizacionPorComa.LOW,
        "sin_aposiciones": """
            City officials announced a new infrastructure plan on Monday.
            The project will improve roads and public transportation across five districts.
            Residents welcomed the news and asked about the timeline for construction.
            Work is expected to begin next spring and finish within eighteen months.
            """,
        "con_aposiciones": """
            City officials, speaking at a press conference, announced a new infrastructure plan on Monday.
            The project, backed by federal funding, will improve roads and public transportation across five districts.
            Residents, gathered outside city hall, welcomed the news and asked about the timeline for construction.
            Work, according to the mayor, is expected to begin next spring and finish within eighteen months.
            """
    },
    {
        "nombre": "Documentacion tecnica",
        "penalizacion": PenalizacionPorComa.MEDIUM,
        "sin_aposiciones": """
            The authentication module validates user credentials against the encrypted database before granting access.
            Each request is assigned a unique token that expires after a configurable session duration.
            Failed login attempts trigger a rate limiting mechanism to prevent brute force attacks on the system.
            Administrators can configure the security policies through the management interface provided in the dashboard.
            """,
        "con_aposiciones": """
            The authentication module, built on industry-standard protocols, validates user credentials against the encrypted database before granting access.
            Each request is assigned a unique token, generated via SHA-256 hashing, that expires after a configurable session duration.
            Failed login attempts, logged for audit purposes, trigger a rate limiting mechanism to prevent brute force attacks on the system.
            Administrators, with appropriate permissions, can configure the security policies through the management interface provided in the dashboard.
            """
    },
    {
        "nombre": "Texto narrativo simple",
        "penalizacion": PenalizacionPorComa.LOW,
        "sin_aposiciones": """
            Maria walked to the market early in the morning to buy fresh vegetables.
            She chose tomatoes and onions and a bunch of herbs for the evening meal.
            The vendor gave her a small discount because she was a regular customer.
            She thanked him and went home to start cooking before noon.
            """,
        "con_aposiciones": """
            Maria, a young woman from the neighborhood, walked to the market early in the morning to buy fresh vegetables.
            She chose tomatoes and onions and a bunch of herbs, all locally grown, for the evening meal.
            The vendor, a friendly old man, gave her a small discount because she was a regular customer.
            She thanked him and went home, basket in hand, to start cooking before noon.
            """
    },
]
