from flask import abort, flash, redirect, render_template

from yacut import app
from yacut.forms import URLMapForm
from yacut.models import ShortGenerateError, URLMap, ValidationError

SHORT_MESSAGE = 'Ваша короткая ссылка готова:'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        return render_template(
            'index.html', form=form,
            urlmap=URLMap.create(
                original=form.original_link.data,
                short=form.data.get('custom_id')
            )
        )
    except ValidationError:
        abort(500)
    except ShortGenerateError as error:
        flash(str(error))
        return render_template('index.html', form=form)


@app.route('/<string:short>')
def short_url(short):
    return redirect(URLMap.get_original_or_404(short))
