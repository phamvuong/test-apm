from flask import Flask, jsonify
import random

age=('21', '22', '23', '24', '25')
country=('sweden', 'canada', 'england', 'italy', 'france')
exp=('1', '2', '3', '4', '5', '6')
hobby=('programming', 'football', 'foosball', 'table tenis', 'swimming')
job=('freelancer', 'sre', 'devops')
name=('andy', 'jorge', 'bobby', 'vuong', 'minh', 'tien', 'anh', 'tam')
lastname=('mcky', 'bush', 'deni', 'pham', 'nguyen')

app = Flask(__name__)

@app.route('/')
def index():
  return jsonify(age=random.choice(age),
                 country=random.choice(country),
                 experience_in_years=random.choice(exp),
                 hobbies=random.sample(hobby,2),
                 job=random.choice(job),
                 name=random.choice(name),
                 surname=random.choice(lastname))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
