# Generated by Django 4.2.4 on 2023-09-30 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Faculty', '0006_alter_kcseresults_grade_alter_kcseresults_subject_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kcseresults',
            name='grade',
            field=models.CharField(choices=[('B-', 'B-'), ('D', 'D'), ('C', 'C'), ('A-', 'A-'), ('A', 'A'), ('D-', 'D-'), ('B', 'B'), ('C+', 'C+'), ('B+', 'B+'), ('C-', 'C-'), ('E', 'E'), ('D+', 'D+')], max_length=100),
        ),
        migrations.AlterField(
            model_name='kcseresults',
            name='subject',
            field=models.CharField(choices=[('Computer Studies', 'Computer Studies'), ('English', 'English'), ('Geography', 'Geography'), ('Business Studies', 'Business Studies'), ('Christian Religious Education', 'Christian Religious Education'), ('Agriculture', 'Agriculture'), ('Mathematics', 'Mathematics'), ('Building and Construction', 'Building and Construction'), ('Kiswahili', 'Kiswahili'), ('Home Science', 'Home Science'), ('Biology', 'Biology'), ('Physics', 'Physics'), ('Drawing and Design', 'Drawing and Design'), ('Chemistry', 'Chemistry'), ('French', 'French')], max_length=100),
        ),
        migrations.AlterField(
            model_name='lecturerevaluation',
            name='answers_questions_clearly',
            field=models.CharField(choices=[('Poor', 'Poor'), ('Excellent', 'Excellent'), ('Good', 'Good'), ('Too Much', 'Too Much'), ('Adequate', 'Adequate')], max_length=100),
        ),
        migrations.AlterField(
            model_name='lecturerevaluation',
            name='asks_questions_of_class',
            field=models.CharField(choices=[('Poor', 'Poor'), ('Excellent', 'Excellent'), ('Good', 'Good'), ('Too Much', 'Too Much'), ('Adequate', 'Adequate')], max_length=100),
        ),
        migrations.AlterField(
            model_name='lecturerevaluation',
            name='available_to_students_after_class',
            field=models.CharField(choices=[('Poor', 'Poor'), ('Excellent', 'Excellent'), ('Good', 'Good'), ('Too Much', 'Too Much'), ('Adequate', 'Adequate')], max_length=100),
        ),
        migrations.AlterField(
            model_name='lecturerevaluation',
            name='encourages_questions_and_comments',
            field=models.CharField(choices=[('Poor', 'Poor'), ('Excellent', 'Excellent'), ('Good', 'Good'), ('Too Much', 'Too Much'), ('Adequate', 'Adequate')], max_length=100),
        ),
        migrations.AlterField(
            model_name='lecturerevaluation',
            name='explains_concepts_clearly',
            field=models.CharField(choices=[('Poor', 'Poor'), ('Excellent', 'Excellent'), ('Good', 'Good'), ('Too Much', 'Too Much'), ('Adequate', 'Adequate')], max_length=100),
        ),
        migrations.AlterField(
            model_name='lecturerevaluation',
            name='explains_how_each_topic_fits_in',
            field=models.CharField(choices=[('Poor', 'Poor'), ('Excellent', 'Excellent'), ('Good', 'Good'), ('Too Much', 'Too Much'), ('Adequate', 'Adequate')], max_length=100),
        ),
        migrations.AlterField(
            model_name='lecturerevaluation',
            name='facilitates_discussions_during_lecture',
            field=models.CharField(choices=[('Poor', 'Poor'), ('Excellent', 'Excellent'), ('Good', 'Good'), ('Too Much', 'Too Much'), ('Adequate', 'Adequate')], max_length=100),
        ),
        migrations.AlterField(
            model_name='lecturerevaluation',
            name='gestures_while_speaking',
            field=models.CharField(choices=[('Poor', 'Poor'), ('Excellent', 'Excellent'), ('Good', 'Good'), ('Too Much', 'Too Much'), ('Adequate', 'Adequate')], max_length=100),
        ),
        migrations.AlterField(
            model_name='lecturerevaluation',
            name='gives_multiple_examples',
            field=models.CharField(choices=[('Poor', 'Poor'), ('Excellent', 'Excellent'), ('Good', 'Good'), ('Too Much', 'Too Much'), ('Adequate', 'Adequate')], max_length=100),
        ),
        migrations.AlterField(
            model_name='lecturerevaluation',
            name='gives_preliminary_overview_of_lecture',
            field=models.CharField(choices=[('Poor', 'Poor'), ('Excellent', 'Excellent'), ('Good', 'Good'), ('Too Much', 'Too Much'), ('Adequate', 'Adequate')], max_length=100),
        ),
        migrations.AlterField(
            model_name='lecturerevaluation',
            name='moves_about_while_lecturing',
            field=models.CharField(choices=[('Poor', 'Poor'), ('Excellent', 'Excellent'), ('Good', 'Good'), ('Too Much', 'Too Much'), ('Adequate', 'Adequate')], max_length=100),
        ),
        migrations.AlterField(
            model_name='lecturerevaluation',
            name='points_out_practical_applications',
            field=models.CharField(choices=[('Poor', 'Poor'), ('Excellent', 'Excellent'), ('Good', 'Good'), ('Too Much', 'Too Much'), ('Adequate', 'Adequate')], max_length=100),
        ),
        migrations.AlterField(
            model_name='lecturerevaluation',
            name='proceeds_at_good_pace_for_topic',
            field=models.CharField(choices=[('Poor', 'Poor'), ('Excellent', 'Excellent'), ('Good', 'Good'), ('Too Much', 'Too Much'), ('Adequate', 'Adequate')], max_length=100),
        ),
        migrations.AlterField(
            model_name='lecturerevaluation',
            name='projects_confidence',
            field=models.CharField(choices=[('Poor', 'Poor'), ('Excellent', 'Excellent'), ('Good', 'Good'), ('Too Much', 'Too Much'), ('Adequate', 'Adequate')], max_length=100),
        ),
        migrations.AlterField(
            model_name='lecturerevaluation',
            name='promotes_critical_thinking',
            field=models.CharField(choices=[('Poor', 'Poor'), ('Excellent', 'Excellent'), ('Good', 'Good'), ('Too Much', 'Too Much'), ('Adequate', 'Adequate')], max_length=100),
        ),
        migrations.AlterField(
            model_name='lecturerevaluation',
            name='repeats_difficult_ideas',
            field=models.CharField(choices=[('Poor', 'Poor'), ('Excellent', 'Excellent'), ('Good', 'Good'), ('Too Much', 'Too Much'), ('Adequate', 'Adequate')], max_length=100),
        ),
        migrations.AlterField(
            model_name='lecturerevaluation',
            name='shows_facial_expression',
            field=models.CharField(choices=[('Poor', 'Poor'), ('Excellent', 'Excellent'), ('Good', 'Good'), ('Too Much', 'Too Much'), ('Adequate', 'Adequate')], max_length=100),
        ),
        migrations.AlterField(
            model_name='lecturerevaluation',
            name='signals_transition_to_new_topic',
            field=models.CharField(choices=[('Poor', 'Poor'), ('Excellent', 'Excellent'), ('Good', 'Good'), ('Too Much', 'Too Much'), ('Adequate', 'Adequate')], max_length=100),
        ),
        migrations.AlterField(
            model_name='lecturerevaluation',
            name='speaks_expressively_or_emphatically',
            field=models.CharField(choices=[('Poor', 'Poor'), ('Excellent', 'Excellent'), ('Good', 'Good'), ('Too Much', 'Too Much'), ('Adequate', 'Adequate')], max_length=100),
        ),
        migrations.AlterField(
            model_name='lecturerevaluation',
            name='states_lecture_objectives',
            field=models.CharField(choices=[('Poor', 'Poor'), ('Excellent', 'Excellent'), ('Good', 'Good'), ('Too Much', 'Too Much'), ('Adequate', 'Adequate')], max_length=100),
        ),
        migrations.AlterField(
            model_name='lecturerevaluation',
            name='stays_on_theme_of_lecture',
            field=models.CharField(choices=[('Poor', 'Poor'), ('Excellent', 'Excellent'), ('Good', 'Good'), ('Too Much', 'Too Much'), ('Adequate', 'Adequate')], max_length=100),
        ),
        migrations.AlterField(
            model_name='lecturerevaluation',
            name='stresses_important_concepts',
            field=models.CharField(choices=[('Poor', 'Poor'), ('Excellent', 'Excellent'), ('Good', 'Good'), ('Too Much', 'Too Much'), ('Adequate', 'Adequate')], max_length=100),
        ),
        migrations.AlterField(
            model_name='lecturerevaluation',
            name='ties_in_primary_objectives_of_the_course',
            field=models.CharField(choices=[('Poor', 'Poor'), ('Excellent', 'Excellent'), ('Good', 'Good'), ('Too Much', 'Too Much'), ('Adequate', 'Adequate')], max_length=100),
        ),
        migrations.AlterField(
            model_name='lecturerevaluation',
            name='uses_concrete_examples_of_concepts',
            field=models.CharField(choices=[('Poor', 'Poor'), ('Excellent', 'Excellent'), ('Good', 'Good'), ('Too Much', 'Too Much'), ('Adequate', 'Adequate')], max_length=100),
        ),
        migrations.AlterField(
            model_name='lecturerevaluation',
            name='uses_humor',
            field=models.CharField(choices=[('Poor', 'Poor'), ('Excellent', 'Excellent'), ('Good', 'Good'), ('Too Much', 'Too Much'), ('Adequate', 'Adequate')], max_length=100),
        ),
        migrations.AlterField(
            model_name='noticeboard',
            name='addressed_to',
            field=models.CharField(choices=[('ADMIN', 'ADMIN'), ('STUDENT', 'STUDENT'), ('LEC', 'LEC'), ('HOD', 'HOD'), ('FINANCE', 'FINANCE'), ('DEAN', 'DEAN')], default='STUDENT', max_length=100),
        ),
    ]
