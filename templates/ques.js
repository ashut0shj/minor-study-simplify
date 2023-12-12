// const container = document.querySelector('.container');
// const questionElement = document.querySelector('.question');
// const answerElement = document.querySelector('.answer');

// fetch('questions.txt')
//     .then((res) => res.text())
//     .then((csvData) => {
//         // Parse CSV data
//         const parsedData = Papa.parse(csvData, { header: true });

//         // Convert the parsed data into the format you need for your quiz game
//         const questionsAndAnswers = parsedData.data;

//         // Display each question and answer
//         let count = 1;
//         questionsAndAnswers.forEach((qa) => {
//             questionElement.textContent = `${count}. ${qa.question}`;
//             answerElement.textContent = `Answer: ${qa.answer}`;
//             count++;

//             // Append the cloned elements to the container
//             const clone = container.cloneNode(true);
//             document.body.appendChild(clone);
//         });
//     });
fetch('questions.txt')
    .then((res) => res.text())
    .then((csvData) => {
        // Parse CSV data
        const parsedData = Papa.parse(csvData, { delimiter: '$', header: true });

        // Convert the parsed data into the format you need for your quiz game
        const questionsAndAnswers = parsedData.data;

        // Display each question and answer
        let count = 1;
        questionsAndAnswers.forEach((qa) => {
            // Create new elements for each question and answer
            const newContainer = document.createElement('div');
            newContainer.classList.add('container');

            const newQuestionElement = document.createElement('p');
            newQuestionElement.classList.add('question');
            newQuestionElement.textContent = `${count}. ${qa.question}`;

            const newAnswerElement = document.createElement('p');
            newAnswerElement.classList.add('answer');
            newAnswerElement.textContent = `Answer: ${qa.answer}`;

            // Append the new elements to the body
            newContainer.appendChild(newQuestionElement);
            newContainer.appendChild(newAnswerElement);
            document.body.appendChild(newContainer);

            count++;
        });
    });
