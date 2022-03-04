from datetime import datetime

from flask import Blueprint, render_template, request, url_for
from werkzeug.utils import redirect
from werkzeug.utils import secure_filename # for fileupload Function

from .. import db
from ..forms import QuestionForm, AnswerForm
from ..models import Question

bp = Blueprint('question', __name__, url_prefix='/question')

# 질문들을 리스팅한다.
@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)  # 페이지
    #database에서 자료들(lists)을 가져온다.
    question_list = Question.query.order_by(Question.create_date.desc())
    question_list = question_list.paginate(page, per_page=10)
    #보여줄 자료를 만든 후(전달 대상(context), question_list)에 보여주는 것( html) 을 호출한다.
    return render_template('question/question_list.html', question_list=question_list)


@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    # 특정 한 개의 질문사항...
    question = Question.query.get_or_404(question_id)
    # 질문에 대한 상세 정보를 출력한다.  질문에 대한 내용과. 그에 따른 답변사항.. 및 새로운 답변을 달 수 있도록 Form 로 연결해서 보낸다.
    return render_template('question/question_detail.html', question=question, form=form)


@bp.route('/create/', methods=('GET', 'POST'))
def create():
    #질문 등록할 수 있는 Form ...
    form = QuestionForm()
    # requests는 자동은로 넘어오고, 잡근 가능한듯..Routing...
    if request.method == 'POST' and form.validate_on_submit():
        # form문에서 넘어오면..(submit 후).... 데이터베이스 모델...Question.. 을 생성...models.py...
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now())
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form=form)


#파일업로드 처리
@bp.route('/FileUpload', methods=('GET', 'POST'))
def upload_file():
    form = QuestionForm()
    if request.method == 'POST':
        f = request.files['file']
        #저장할 경로 + 파일명
        f.save( secure_filename(f.filename) )
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form=form)



