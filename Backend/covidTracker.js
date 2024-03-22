const Apify = require('apify');

// Set API token
Apify.client.setOptions({ token: '<YOUR_API_TOKEN>' });

// Prepare actor input
const input = {
    email: "zuzka@apify.com"
};

// Run the actor
const run = Apify.call('zuzka/covid-in', input);

// Print actor output (if any)
console.log('Output');
console.dir(run.output);

// Fetch and print actor results from the run's dataset (if any)
console.log('Results from dataset');
const dataset = Apify.openDataset(run.defaultDatasetId, { forceCloud: true });
dataset.forEach(async (item, index) => {
    console.log(JSON.stringify(item));
});