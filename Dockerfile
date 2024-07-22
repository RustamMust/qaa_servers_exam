FROM python:3.12-alpine

WORKDIR /test_dir

COPY requirements.txt .
COPY conftest.py .

RUN mkdir -p /test_dir/global_constants
RUN mkdir -p /test_dir/pages
RUN mkdir -p /test_dir/tests
RUN mkdir -p /test_dir/allure-results

COPY global_constants/constants.py /test_dir/global_constants/

COPY pages/authorization_page.py /test_dir/pages/
COPY pages/base_page.py /test_dir/pages/
COPY pages/main_servers_page.py /test_dir/pages/
COPY pages/profile_page.py /test_dir/pages/
COPY pages/registration_page.py /test_dir/pages/

COPY tests/test_servers_page.py /test_dir/tests/

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/test_dir


CMD ["pytest", "tests/", "--alluredir=allure-results"]
