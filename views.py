from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from .models import Course, Question, Choice, Submission


# Function-based course list view
def popular_course_list(request):
    course_list = Course.objects.order_by('-total_enrollment')[:10]
    return render(request, 'onlinecourse/course_list.html', {'course_list': course_list})


# Function-based course details view
def course_details(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
        return render(request, 'onlinecourse/course_details_bootstrap.html', {'course': course})
    except Course.DoesNotExist:
        raise Http404("No course matches the given id.")


# Function-based enroll view
def enroll(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=course_id)
        course.total_enrollment += 1
        course.save()
        return HttpResponseRedirect(reverse('onlinecourse:course_details', args=(course.id,)))


# Submit exam
def submit(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=course_id)
        selected_choices = request.POST.getlist('choice')

        submission = Submission.objects.create(
            user=request.user,
            course=course
        )

        total_score = 0

        for question in Question.objects.filter(lesson__course=course):
            correct_choices = set(
                question.choice_set.filter(is_correct=True).values_list('id', flat=True)
            )
            selected_for_question = set(map(int, selected_choices)) & set(
                question.choice_set.values_list('id', flat=True)
            )

            if correct_choices == selected_for_question:
                total_score += question.grade

        submission.score = total_score
        submission.save()
        submission.choices.set(selected_choices)

        return redirect('onlinecourse:show_exam_result', submission_id=submission.id)


# Show exam result
def show_exam_result(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)
    course = submission.course
    questions = Question.objects.filter(lesson__course=course)

    total_possible = sum(q.grade for q in questions)

    context = {
        'course': course,
        'submission': submission,
        'score': submission.score,
        'total_possible': total_possible,
    }

    return render(request, 'onlinecourse/exam_result.html', context)
