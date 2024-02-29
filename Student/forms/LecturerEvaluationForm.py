from django import forms

from Faculty.models import LecturerEvaluation

choices = {
    ('Excellent', 'Excellent'),
    ('Good', 'Good'),
    ('Adequate', 'Adequate'),
    ('Poor', 'Poor'),
    ('Too Much', 'Too Much'),
}


class LecEvaluationForm(forms.ModelForm):
    promotes_critical_thinking = forms.ChoiceField(widget=forms.RadioSelect(), choices=choices)
    ties_in_primary_objectives_of_the_course = forms.ChoiceField(widget=forms.RadioSelect(), choices=choices)
    explains_concepts_clearly = forms.ChoiceField(widget=forms.RadioSelect(), choices=choices)
    uses_concrete_examples_of_concepts = forms.ChoiceField(widget=forms.RadioSelect(), choices=choices)
    gives_multiple_examples = forms.ChoiceField(widget=forms.RadioSelect(), choices=choices)
    points_out_practical_applications = forms.ChoiceField(widget=forms.RadioSelect(), choices=choices)
    stresses_important_concepts = forms.ChoiceField(widget=forms.RadioSelect(), choices=choices)
    repeats_difficult_ideas = forms.ChoiceField(widget=forms.RadioSelect(), choices=choices)
    encourages_questions_and_comments = forms.ChoiceField(widget=forms.RadioSelect(), choices=choices)
    answers_questions_clearly = forms.ChoiceField(widget=forms.RadioSelect(), choices=choices)
    available_to_students_after_class = forms.ChoiceField(widget=forms.RadioSelect(), choices=choices)
    asks_questions_of_class = forms.ChoiceField(widget=forms.RadioSelect(), choices=choices)
    facilitates_discussions_during_lecture = forms.ChoiceField(widget=forms.RadioSelect(), choices=choices)
    proceeds_at_good_pace_for_topic = forms.ChoiceField(widget=forms.RadioSelect(), choices=choices)
    stays_on_theme_of_lecture = forms.ChoiceField(widget=forms.RadioSelect(), choices=choices)
    states_lecture_objectives = forms.ChoiceField(widget=forms.RadioSelect(), choices=choices)
    gives_preliminary_overview_of_lecture = forms.ChoiceField(widget=forms.RadioSelect(), choices=choices)
    signals_transition_to_new_topic = forms.ChoiceField(widget=forms.RadioSelect(), choices=choices)
    explains_how_each_topic_fits_in = forms.ChoiceField(widget=forms.RadioSelect(), choices=choices)
    projects_confidence = forms.ChoiceField(widget=forms.RadioSelect(), choices=choices)
    speaks_expressively_or_emphatically = forms.ChoiceField(widget=forms.RadioSelect(), choices=choices)
    moves_about_while_lecturing = forms.ChoiceField(widget=forms.RadioSelect(), choices=choices)
    gestures_while_speaking = forms.ChoiceField(widget=forms.RadioSelect(), choices=choices)
    shows_facial_expression = forms.ChoiceField(widget=forms.RadioSelect(), choices=choices)
    uses_humor = forms.ChoiceField(widget=forms.RadioSelect(), choices=choices)

    class Meta:
        model = LecturerEvaluation
        fields = ["promotes_critical_thinking", "ties_in_primary_objectives_of_the_course", "explains_concepts_clearly", "uses_concrete_examples_of_concepts", "gives_multiple_examples",
                  "points_out_practical_applications", "stresses_important_concepts", "repeats_difficult_ideas",
                  "encourages_questions_and_comments", "answers_questions_clearly", "available_to_students_after_class",
                  "asks_questions_of_class", "facilitates_discussions_during_lecture", "proceeds_at_good_pace_for_topic",
                  "stays_on_theme_of_lecture", "states_lecture_objectives", "gives_preliminary_overview_of_lecture",
                  "signals_transition_to_new_topic", "explains_how_each_topic_fits_in", "projects_confidence",
                  "speaks_expressively_or_emphatically", "moves_about_while_lecturing", "gestures_while_speaking", "shows_facial_expression", "uses_humor"
                  ]
