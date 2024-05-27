import joblib
from flask import Flask, render_template, request

app = Flask(__name__)
model = joblib.load('student_performance_model.pkl')
passing_threshold = 65  # Define threshold explicitly

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Get scores
            scores = {
                'math': float(request.form['math']),
                'writing': float(request.form['writing']),
                'history': float(request.form['history']),
                'physics': float(request.form['physics']),
                'chemistry': float(request.form['chemistry']),
                'biology': float(request.form['biology']),
                'english': float(request.form['english'])
            }

            # Map categorical features
            features = [
                1 if request.form['gender'] == 'male' else 2,
                {'group A': 1, 'group B': 2, 'group C': 3, 'group D': 4, 'group E': 5}[request.form['race_ethnicity']],
                1 if request.form['test_preparation_course'] == 'completed' else 0
            ] + list(scores.values())  # Combine features with scores

        except (ValueError, KeyError):
            return render_template('index.html', error="Invalid or missing input. Please check your entries.")

        # Calculate mean score directly from the dictionary
        mean_score = sum(scores.values()) / len(scores)

        # Make prediction using the  features list
        prediction = model.predict([features])[0]

        # Determine pass/fail based on  model prediction and mean score
        if prediction == 1 and mean_score >= passing_threshold:
            result = "Pass"
        else:
            result = "Fail"

        return render_template('result.html', result=result, mean_score=mean_score)

    return render_template('index.html', error=None)


if __name__ == '__main__':
    app.run(debug=True)
