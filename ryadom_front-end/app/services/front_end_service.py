from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()


class FrontEndService:
    
    def __init__(self):
        self.templates = Jinja2Templates(directory='app/templates')

    def render_template(self, template_name: str, request):
        """
        Рендер шаблона с контекстом

        Args:
            template_name: имя шаблона
            context: данные для шаблона

        Returns:
            TemplateResponse: ответ с отрендеренным шаблоном
        """
        return self.templates.TemplateResponse(template_name, {'request': request})