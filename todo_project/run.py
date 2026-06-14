from todo_project import app
from prometheus_flask_exporter import PrometheusMetrics

metrics = PrometheusMetrics(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
