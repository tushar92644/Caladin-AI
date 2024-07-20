def construct_prompt(pdf_text):
    examples = """
    # Example 1:
    # Research paper: Study on the effects of drug A on disease B.
    # Domain 1: Risk of bias arising from the randomization process
    # 1.1 Was the allocation sequence random? Yes, computer-generated randomization.
    # 1.2 Was the allocation sequence concealed until participants were enrolled and assigned to interventions? Yes, using sealed opaque envelopes.
    # 1.3 Did baseline differences between intervention groups suggest a problem with the randomization process? No, baseline characteristics were similar.
    # 1.4 Risk-of-bias judgement: Low risk.

    # Example 2:
    # Research paper: Analysis of the impact of lifestyle changes on health outcomes.
    # Domain 2: Risk of bias due to deviations from the intended interventions
    # 2.1 Were participants aware of their assigned intervention during the trial? Yes.
    # 2.2 Were carers and people delivering the interventions aware of participants' assigned intervention during the trial? Yes.
    # 2.3 Were there deviations from the intended intervention that arose because of the trial context? Yes, some non-adherence occurred.
    # 2.4 Were these deviations likely to have affected the outcome? Possibly.
    # 2.5 Were these deviations from intended intervention balanced between groups? Yes.
    # 2.6 Was an appropriate analysis used to estimate the effect of assignment to intervention? Yes, intention-to-treat analysis.
    # 2.7 Risk-of-bias judgement: Some concerns.

    Detailed Example for Domain 1:
    Domain 1: Risk of bias arising from the randomization process
    Signalling questions Elaboration Response options
    1.1 Was the allocation sequence random? 
        Yes, a random component was used such as computer-generated random numbers or coin tossing.
        No, the sequence is predictable or based on dates or patient record numbers.
        No information, only a statement that the study is randomized.
        Probably yes or Probably no can be used based on context and the trial's conduct.
        Y/PY/PN/N/NI
    1.2 Was the allocation sequence concealed until participants were enrolled and assigned to interventions?
        Yes, if remote or centrally administered methods were used, or envelopes/drug containers were handled properly.
        No, if there is reason to suspect the allocation was known.
        Y/PY/PN/N/NI
    1.3 Did baseline differences between intervention groups suggest a problem with the randomization process?
        No, if no imbalances are apparent or are compatible with chance.
        Yes, if imbalances suggest issues with randomization or if there are significant differences unlikely due to chance.
        No information, if baseline information is not available.
        Y/PY/PN/N/NI
    Risk-of-bias judgement: Low / High / Some concerns
    """

    prompt_parts = [
        "You are an expert scientific researcher with extensive experience in conducting systematic literature surveys and meta-analyses. "
        "Your task is to analyze the following research paper using the Revised Cochrane risk-of-bias tool for randomized trials (RoB 2). "
        "Please provide detailed answers to the following questions for each domain of bias,while giving response highlight the Domain in bigger font size:To display a more readable format to the user\n\n"
        "Research paper:\n"
        f"{pdf_text}\n\n"
        "Examples for reference:\n"
        f"{examples}\n\n"
        "Domain 1: Risk of bias arising from the randomization process\n"
            "1.1 Was the allocation sequence random?\n"
            "1.2 Was the allocation sequence concealed until participants were enrolled and assigned to interventions?\n"
            "1.3 Did baseline differences between intervention groups suggest a problem with the randomization process?\n"
            "1.4 Risk-of-bias judgement\n"
            "1.5 Optional: What is the predicted direction of bias arising from the randomization process?\n\n"
            "Domain 2: Risk of bias due to deviations from the intended interventions (effect of assignment to intervention)\n"
            "2.1 Were participants aware of their assigned intervention during the trial?\n"
            "2.2 Were carers and people delivering the interventions aware of participants' assigned intervention during the trial?\n"
            "2.3 If Y/PY/NI to 2.1 or 2.2: Were there deviations from the intended intervention that arose because of the trial context?\n"
            "2.4 If Y/PY to 2.3: Were these deviations likely to have affected the outcome?\n"
            "2.5 If Y/PY/NI to 2.4: Were these deviations from intended intervention balanced between groups?\n"
            "2.6 Was an appropriate analysis used to estimate the effect of assignment to intervention?\n"
            "2.7 If N/PN/NI to 2.6: Was there potential for a substantial impact (on the result) of the failure to analyse participants in the group to which they were randomized?\n"
            "2.8 Risk-of-bias judgement\n"
            "2.9 Optional: What is the predicted direction of bias due to deviations from intended interventions?\n\n"
            "Domain 2.1: Risk of bias due to deviations from the intended interventions (effect of adhering to intervention)\n"
            "2.1.1 Were participants aware of their assigned intervention during the trial?\n"
            "2.1.2 Were carers and people delivering the interventions aware of participants' assigned intervention during the trial?\n"
            "2.1.3 [If applicable:] If Y/PY/NI to 2.1.1 or 2.1.2: Were important non-protocol interventions balanced across intervention groups?\n"
            "2.1.4 [If applicable:] Were there failures in implementing the intervention that could have affected the outcome?\n"
            "2.1.5 [If applicable:] Was there non-adherence to the assigned intervention regimen that could have affected participants’ outcomes?\n"
            "2.1.6 If N/PN/NI to 2.1.3, or Y/PY/NI to 2.1.4 or 2.1.5: Was an appropriate analysis used to estimate the effect of adhering to the intervention?\n"
            "2.1.7 Risk-of-bias judgement\n"
            "2.1.8 Optional: What is the predicted direction of bias due to deviations from intended interventions?\n\n"
            "Domain 3: Risk of bias due to missing outcome data\n"
            "3.1 Were data for this outcome available for all, or nearly all, participants randomized?\n"
            "3.2 If N/PN/NI to 3.1: Is there evidence that the result was not biased by missing outcome data?\n"
            "3.3 If N/PN to 3.2: Could missingness in the outcome depend on its true value?\n"
            "3.4 If Y/PY/NI to 3.3: Is it likely that missingness in the outcome depended on its true value?\n"
            "3.5 Risk-of-bias judgement\n"
            "3.6 Optional: What is the predicted direction of bias due to missing outcome data?\n\n"
            "Domain 4: Risk of bias in measurement of the outcome\n"
            "4.1 Was the method of measuring the outcome inappropriate?\n"
            "4.2 Could measurement or ascertainment of the outcome have differed between intervention groups?\n"
            "4.3 If N/PN/NI to 4.1 and 4.2: Were outcome assessors aware of the intervention received by study participants?\n"
            "4.4 If Y/PY/NI to 4.3: Could assessment of the outcome have been influenced by knowledge of intervention received?\n"
            "4.5 If Y/PY/NI to 4.4: Is it likely that assessment of the outcome was influenced by knowledge of intervention received?\n"
            "4.6 Risk-of-bias judgement\n"
            "4.7 Optional: What is the predicted direction of bias in measurement of the outcome?\n\n"
            "Domain 5: Risk of bias in selection of the reported result\n"
            "5.1 Were the data that produced this result analysed in accordance with a pre-specified analysis plan that was finalized before unblinded outcome data were available for analysis?\n"
            "5.2 Is the numerical result being assessed likely to have been selected, on the basis of the results, from multiple eligible outcome measurements (e.g. scales, definitions, time points) within the outcome domain?\n"
            "5.3 Is the numerical result being assessed likely to have been selected, on the basis of the results, from multiple eligible analyses of the data?\n"
            "5.4 Risk-of-bias judgement\n"
            "5.5 Optional: What is the predicted direction of bias due to selection of the reported result?\n\n"
    ]

    # Concatenate the prompt parts into a single string
    prompt_text = ''.join(prompt_parts)
    return prompt_text
