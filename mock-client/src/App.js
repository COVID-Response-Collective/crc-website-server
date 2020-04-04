/** @jsx jsx */
import { jsx } from '@emotion/core'
import {useState} from 'react'
import { Grid, TextField, Button } from '@material-ui/core'

const App = () => {
  const [name, setName] = useState("")
  const [region, setRegion] = useState("")
  const [role, setRole] = useState("")
  const [title, setTitle] = useState("")
  const [agency, setAgency] = useState("")
  const [jurisdiction, setJurisdiction] = useState("")
  const [email, setEmail] = useState("")
  const [phone, setPhone] = useState("")
  const [details, setDetails] = useState("")
  return (
    <Grid
      container
      direction="column"
      justify="center"
      alignItems="center"
    >
      <h2>API Test Form: Resource Request</h2>
      <form onSubmit={e => {
        e.preventDefault()

       fetch('http://0.0.0.0:5000/request/create', {
         method: 'POST',
         mode: 'cors',
         headers: {
           'Accept': 'application/json',
           'Content-Type': 'application/json'
         },
         body: JSON.stringify({
           name: name,
           region: region,
           role: role,
           title: title,
           agency: agency,
           jurisdiction: jurisdiction,
           email: email,
           phone: phone,
           details: details
         })
       }) 
      }}>
        <div><TextField label="Name" onchange={e => setName(e.target.value)}/></div>
        <div><TextField label="Region" onchange={e => setRegion(e.target.value)}/></div>
        <div><TextField label="Role" onchange={e => setRole(e.target.value)}/></div>
        <div><TextField label="Title" onchange={e => setTitle(e.target.value)}/></div>
        <div><TextField label="Agency" onchange={e => setAgency(e.target.value)}/></div>
        <div><TextField label="Jurisdiction" onchange={e => setJurisdiction(e.target.value)}/></div>
        <div><TextField label="email" onchange={e => setEmail(e.target.value)}/></div>
        <div><TextField label="Phone" onchange={e => setPhone(e.target.value)}/></div>
        <div><TextField label="Details" onchange={e => setDetails(e.target.value)}/></div>
        <div><Button type="submit" variant="contained">Send</Button></div>
      </form>
    </Grid>
  )
}
export default App;
