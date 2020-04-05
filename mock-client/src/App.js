/** @jsx jsx */
import { jsx } from '@emotion/core'
import {useState} from 'react'
//import { Grid, TextField, Button } from '@material-ui/core'
import { Button, Form, Row, Col, InputGroup } from 'react-bootstrap';
import DatePicker from 'react-datepicker';

const App = () => {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [phone, setPhone] = useState('')
  const [role, setRole] = useState('')
  const [title, setTitle] = useState('')
  const [agency, setAgency] = useState('')
  const [jurisdiction, setJurisdiction] = useState('')
  const [type, setType] = useState('')

  /* Grocery-Specific Fields */
  const [items, setItems] = useState('')
  const [allergies, setAllergies] = useState('')

  /* Funds-Specific Fields */
  const [amount, setAmount] = useState(0.00)
  const [reason, setReason] = useState('')

  /* In-Home Services-Specific Fields */
  const [inHomeType, setInHomeType] = useState('')

  /* Used By Both In-Home Services and Pet Services */
  const [frequency, setFrequency] = useState('ONE TIME')

  /* Used By In-Home Services, Pet Services, and Other */
  const [description, setDescription] = useState('')

  /* Universal Fields */
  const [isNeededBy, setIsNeededBy] = useState(false)
  const [neededByDate, setNeededByDate] = useState(new Date())
  const [isPublic, setIsPublic] = useState(true)
  const [additionalInfo, setAdditionalInfo] = useState('')

  const [validated, setValidated] = useState(false);

  const handleSubmit = (e) => {
    const form = e.currentTarget;
    if (form.checkValidity() === false) {
      e.preventDefault();
      e.stopPropagation();
    }

    setValidated(true);
  }

  return (
    <div style={{width: '60%', margin: '0 auto'}}>
      <h2 style={{textAlign: 'center'}}>API Test Form: Submit a Request</h2>
      <div style={{padding: '1em', textAlign: 'center'}}>
        <small>DISCLAIMER: At this time, the CRC is only able to fulfill requests for Linn and Benton counties in Oregon. We are actively working on our ability to fulfill requests in other regions of the Pacific Northwest!</small>
      </div>
      <Form noValidate validated={validated} onSubmit={handleSubmit}>
        <Form.Group as={Row} controlId='rrName'>
          <Form.Label column sm={3}>
            Name:
            <sup style={{color: 'red', fontWeight: 'bold'}}>*</sup>
          </Form.Label>
          <Col sm={9}>
            <Form.Control
              required
              type='text'
              placeholder='E.g. John Doe'
              label='firstname'
              onChange={e => setName(e.target.value)}/>
          </Col>
          <Form.Control.Feedback type='invalid'>
            Please enter your name.
          </Form.Control.Feedback>
        </Form.Group>

        <Form.Group as={Row} controlId='rfEmail'>
          <Form.Label required column sm={3}>
            Email Address:
            <sup style={{color: 'red', fontWeight: 'bold'}}>*</sup>
          </Form.Label>
          <Col sm={9}>
            <Form.Control
              required
              type='email'
              placeholder='E.g. me@example.com'
              label='email'
              onChange={e => setEmail(e.target.value)}/>
          </Col>
          <Form.Control.Feedback type='invalid'>
            Please enter a valid email address.
          </Form.Control.Feedback>
        </Form.Group>
        <Form.Group as={Row} controlId='rfPhone'>
          <Form.Label column sm={3}>
            Phone Number:
          </Form.Label>
          <Col sm={9}>
            <Form.Control
              placeholder='E.g. (541) 555-5555'
              label='phone'
              onChange={e => setPhone(e.target.value)}/>
          </Col>
        </Form.Group>
        <Form.Group as={Row} controlId='rfRole'>
          <Form.Label required column sm={3}>
            I am a:
            <sup style={{color: 'red', fontWeight: 'bold'}}>*</sup>
          </Form.Label>
          <Col sm={9}>
            <Form.Control
              required
              as='select'
              label='role'
              defaultValue=''
              onChange={e => setRole(e.target.value)}>
              <option value=''>Select one...</option>
              <option value='COMM MEMBER'>Community Member</option>
              <option value='EM PROF'>Emergency Professional</option>
            </Form.Control>
          </Col>
          <Form.Control.Feedback type='invalid'>
            Please select one.
          </Form.Control.Feedback>
        </Form.Group>
        <Form.Group as={Row} controlId='rfType'>
          <Form.Label column sm={3}>
            I need help with:
            <sup style={{color: 'red', fontWeight: 'bold'}}>*</sup>
          </Form.Label>
          <Col sm={9}>
            <Form.Control
              required
              as='select'
              label='type'
              defaultValue=''
              onChange={e => setType(e.target.value)}>
              <option value=''>Select one...</option>
              <option value='GROCERY'>Food/Groceries</option>
              <option value='FUNDS'>Funds</option>
              <option value='IN HOME'>In-Home Services</option>
              <option value='PETS'>Pet Services</option>
              <option value='OTHER'>Other (Please Describe)</option>
            </Form.Control>
          </Col>
          <Form.Control.Feedback type='invalid'>
            Please select a request type.
          </Form.Control.Feedback>
        </Form.Group>
        {type === 'GROCERY' && (
          <div>
            <Form.Group as={Row} controlId='rfGroceryList'>
              <Form.Label column sm={3}>
                Grocery List:
                <sup style={{color: 'red', fontWeight: 'bold'}}>*</sup>
              </Form.Label>
              <Col sm={9}>
                <Form.Control
                  required
                  as='textarea'
                  placeholder='E.g. 1% milk (2), Sourdough bread (1 loaf)'
                  label='grocery_list'
                  onChange={e => setItems(e.target.value)}/>
              </Col>
              <Form.Control.Feedback type='invalid'>
                Please enter your grocery list.
              </Form.Control.Feedback>
            </Form.Group>
            <Form.Group as={Row} controlId='rfAllergies'>
              <Form.Label column sm={3}>
                Allergies:
              </Form.Label>
              <Col sm={9}>
                <Form.Control
                  as='textarea'
                  placeholder='E.g. peanuts'
                  label='allergies'
                  onChange={e => setAllergies(e.target.value)}/>
              </Col>
            </Form.Group>
          </div>
        )}
        {type === 'FUNDS' && (
          <div>
              <Form.Group as={Row} controlId='rfFundAmount'>
                <Form.Label column sm={3}>
                  How much do you need?
                  <sup style={{color: 'red', fontWeight: 'bold'}}>*</sup>
                </Form.Label>
                <Col sm={9} style={{verticalAlign: 'middle'}}>
                  <InputGroup>
                    <InputGroup.Prepend>
                      <InputGroup.Text id='rfAmountPrepend'>
                        $
                      </InputGroup.Text>
                    </InputGroup.Prepend>
                    <Form.Control
                      type='number'
                      placeholder='E.g. 100.00'
                      label='amount'
                      onChange={e => setAmount(e.target.value)}/>
                  </InputGroup>
                </Col>
              </Form.Group>
            <Form.Group as={Row} controlId='rfFundReason'>
              <Form.Label column sm={3}>
                What do you need the funds for?:
                <sup style={{color: 'red', fontWeight: 'bold'}}>*</sup>
              </Form.Label>
              <Col sm={9}>
                <Form.Control
                  required
                  as='textarea'
                  placeholder='E.g. Rent, paying for utilities'
                  label='reason'
                  onChange={e => setReason(e.target.value)}/>
              </Col>
              <Form.Control.Feedback type='invalid'>
                Please tell us why you need these funds.
              </Form.Control.Feedback>
            </Form.Group>
          </div>
        )}
        {type === 'IN HOME' && (
          <Form.Group as={Row} controlId='rfInHomeServiceType'>
            <Form.Label column sm={3}>
              What kind of in-home request?:
              <sup style={{color: 'red', fontWeight: 'bold'}}>*</sup>
            </Form.Label>
            <Col sm={9}>
              <Form.Control
                required
                as='select'
                label='type'
                defaultValue=''
                onChange={e => setType(e.target.value)}>
                <option value=''>Select one...</option>
                <option value='BABYSITTING'>Babysitting</option>
                <option value='ELDER CARE'>Elder Care</option>
                <option value='HOUSEKEEPING'>Housekeeping</option>
                <option value='OTHER'>Other (Please Describe)</option>
              </Form.Control>
            </Col>
            <Form.Control.Feedback type='invalid'>
              Please select the type of service you need.
            </Form.Control.Feedback>
          </Form.Group>
        )}
        {(type === 'IN HOME' || type === 'PETS' || type === 'OTHER') && (
          <Form.Group as={Row} controlId='rfDescription'>
            <Form.Label column sm={3}>
              Please describe the service you need.
              <sup style={{color: 'red', fontWeight: 'bold'}}>*</sup>
            </Form.Label>
            <Col sm={9}>
              <Form.Control
                required
                as='textarea'
                placeholder='Type here...'
                label='description'
                onChange={e => setDescription(e.target.value)} />
            </Col>
            <Form.Control.Feedback type='invalid'>
              Please describe the service you need.
            </Form.Control.Feedback>
          </Form.Group>
        )}
        {(type === 'IN HOME' || type === 'PETS') && (
          <div>
            <fieldset>
              <Form.Group as={Row} controlId='rfFrequency'>
                <Form.Label as='legend' column sm={3}>
                  Is this a one-time or recurring need?
                  <sup style={{color: 'red', fontWeight: 'bold'}}>*</sup>
                </Form.Label>
                <Col sm={9}>
                  <Form.Check
                    type='radio'
                    label='One-Time'
                    name='rfFrequencyRadios'
                    value='ONE TIME'
                    id='rfFrequencyOneTime'
                    selected
                    onSelect={e => setFrequency(e.target.value)} />
                  <Form.Check
                    type='radio'
                    label='Recurring'
                    name='rfFrequencyRadios'
                    value='RECURRING'
                    id='rfFrequencyRecurring'
                    onSelect={e => setFrequency(e.target.value)} />
                </Col>
              </Form.Group>
            </fieldset>
          </div>
        )}
        {type !== '' && (
          <div style={{paddingTop: '1em'}}>
            <Form.Group as={Row} controlId='rfNeededBy'>
              <Form.Label column sm={3}>
                Do you need this request fulfilled by a specific date?
              </Form.Label>
              <Col sm={3}>
                <Form.Check
                  label='Yes'
                  name='rfIsNeededByCheck'
                  id='rfIsNeededByCheck'
                  onChange={e => setIsNeededBy(!isNeededBy)} />
              </Col>
              {isNeededBy && (
                <Col sm={6}>
                  <Row>
                    <Form.Label column sm={3}>
                      Date:
                      <sup style={{color: 'red', fontWeight: 'bold'}}>*</sup>
                    </Form.Label>
                    <Col sm={9}>
                      <Form.Control
                        required
                        type='date'
                        label='neededByDate'
                        onChange={e => setNeededByDate(e.target.value)} />
                      <Form.Control.Feedback type='invalid'>
                        Please indicate when you need the service fulfilled by.
                      </Form.Control.Feedback>
                    </Col>
                  </Row>
                </Col>
              )}
              <Form.Control.Feedback type='invalid'>
                {neededByDate && 'Please specify when you need this request fulfilled by.'}
              </Form.Control.Feedback>
            </Form.Group>
            <fieldset>
              <Form.Group as={Row} controlId='rfPublic'>
                <Form.Label as='legend' column sm={3}>
                  Who would you like this request to be visible to?
                  <sup style={{color: 'red', fontWeight: 'bold'}}>*</sup>
                </Form.Label>
                <Col sm={9}>
                  <Form.Check
                    type='radio'
                    label='Everyone'
                    name='rfVisibilityRadios'
                    id='rfVisibilityEveryone'
                    selected
                    onSelect={e => setIsPublic(true)} />
                  <Form.Check
                    type='radio'
                    label='CRC Administrators Only'
                    name='rfVisibilityRadios'
                    id='rfVisibilityMods'
                    onSelect={e => setIsPublic(false)} />
                </Col>
              </Form.Group>
            </fieldset>
            <Form.Group controlId='rfAdditionalInfo'>
              <Form.Label>
                Please write anything else that you need us to know to best accommodate your request.
              </Form.Label>
              <Form.Control
                as='textarea'
                placeholder='Type here...'
                label='additionalInfo'
                onChange={e => setAdditionalInfo(e.target.value)} />
            </Form.Group>
          </div>
        )}
        <Button type='submit'>Submit Request</Button>
      </Form>
    </div>
    /*<Grid
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
    </Grid>*/
  )
}
export default App;
