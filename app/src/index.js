import React from "react";
import ReactDOM from "react-dom";
import axios from "axios"
import JSONSchemaForm from "@rjsf/core";

const saveData = ({formData}) => {
    axios.post("http://localhost:8080/save/trapmux", formData, {
headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }})
      .then((response) => {
        return response.data;
      });
};

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { isSchemaLoading: true, schema: undefined, isConfigLoading: true, config: undefined };
  }

  componentDidMount() {
    console.debug("After mount! Let's load data from API...");
	  var name = "trapmux";
	axios.get("http://localhost:8080/schema/" + name, {
headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }}
    ).then(response => {
      this.setState({ schema: response.data });
      this.setState({ isSchemaLoading: false });
    });

	axios.get("http://localhost:8080/load/" + name, {
headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }}
    ).then(response => {
      this.setState({ config: response.data });
      this.setState({ isConfigLoading: false });
    });
  }

  render() {
    const { isConfigLoading, isSchemaLoading, config, schema } = this.state;

    if (isSchemaLoading || isConfigLoading) {
      return <div className="App">Loading...</div>;
    }

    return (
          <JSONSchemaForm onSubmit={saveData} formData={config} schema={schema} />
    );
  }
}


const rootElement = document.getElementById("root");
ReactDOM.render( <App />, rootElement);

