from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect  # Http404, HttpResponse
from django.urls import reverse               # 避免了硬编码, 重定向URL
from django.views import generic              # 通用视图
from django.utils import timezone

from .models import Question, Choice
# Create your views here.

# 改良视图是用下面的类写的通用视图
#  ListView 和 DetailView 这两个视图分别抽象“显示一个对象列表”和
# “显示一个特定类型对象的详细信息页面”这两种概念

# 每个通用视图需要知道它将作用于哪个模型。 这由 model 属性提供
# DetailView 期望从 URL 中捕获名为 "pk" 的主键值，所以我们为通用视图把 question_id 改成 pk
# 默认情况下，通用视图 DetailView 使用一个叫做 <app name>/<model name>_detail.html 的模板
# 这里它将使用 "polls/question_detail.html" 模板。template_name 属性是用来告诉 Django 使用
# 一个指定的模板名字，而不是自动生成的默认名字

# 对于 ListView， 自动生成的 context 变量是 question_list。为了覆盖这个行为，
# 我们提供 context_object_name 属性


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'  # 我们自定义context变量

    def get_queryset(self):
        """Return the last five published questions(not including those set
        to be published in the future)."""
        return Question.objects.filter(pub_date__lte=timezone.now()
                                       ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):      # question 变量会自动提供
    model = Question                         # 捕获名为 "pk" 的主键值,所以视图question_id 改成 pk
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that are't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):      # 捕获名为 "pk" 的主键值,所以视图question_id 改成 pk
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:                                                                     # request.Post是个类字典对象
        selected_choice = question.choice_set.get(pk=request.POST['choice'])  # 这里是返回 Choice 的ID的字符串
    except (KeyError, Choice.DoesNotExist):                                  # 页面没选择按钮则引发错误
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'You did not select a choice.',
        })
    else:
        selected_choice.votes += 1                                            # 获取了对应的对象后,加一票
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        # reverse函数避免了在视图函数中硬编码URL, 参数为想要跳转的视图名和该视图的对应URL模式的参数
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


"""
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]  # 最近5个投票问题
    context = {'latest_question_list': latest_question_list,
               }                                          # it returns an HttpResponse object
    return render(request, 'polls/index.html', context)  # so it will be a shortcuts


def detail(request, question_id):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404('Question does not exist')
    question = get_object_or_404(Question, pk=question_id)  # it's also a shortcuts func
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
"""
