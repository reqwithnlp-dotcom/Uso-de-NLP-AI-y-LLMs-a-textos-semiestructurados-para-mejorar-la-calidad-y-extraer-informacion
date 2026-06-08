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
    }

]
