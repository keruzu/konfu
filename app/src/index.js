import React from "react";
import ReactDOM from "react-dom";
import axios from "axios"
import Form from "./configurator_form";


//const baseUrl = "http://localhost:8080/write?name=src/data/trapmux.json"
  function saveData(formData) {
    axios
      .post("http://localhost:8080/save/trapmux", formData, {
headers: { 'Content-Type': 'application/json', 
     'Access-Control-Allow-Origin': '*'
})
      .then((response) => {
        setPost(response.data);
      });
  }

function getSchema(name) {
	axios.get("http://localhost:8080/schema/" + name, {
headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'
	}})
	.then((response) => { return response.data } );
};
var schema = getSchema("trapmux");

function getConfig(name) {
	axios.get("http://localhost:8080/load/" + name, {
headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'
	}})
	.then((response) => { return response.data } );
};
var ConfigFileData = getConfig("trapmux");

function App() {
	return <Form schema={schema} onSubmit={saveData} formData={ConfigFileData} />;
}

/*
const App = () => {
	const [formData, setFormData] = React.useState(null);
	return <Form schema={schema} onSubmit={saveData} formData={configFileData} 
		onChange={e => setFormData(e.formData)}/>;
}

*/

const rootElement = document.getElementById("root");
ReactDOM.render(<App />, rootElement);

