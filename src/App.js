import React, { useEffect, useState } from 'react';
import logo from './logo.svg';
import './App.css';
import axios from 'axios'
import { Row, List, ListItem, Container, Navbar, NavbarInner, ContentContainer, SideBar, InnerContentContainer } from './styles'
import DataTable from 'react-data-table-component'
const App = () => {
  const [data, setData] = useState(null)
  useEffect(() => {
    axios.get('http://127.0.0.1:5000/get_mmr').then(res => {
      console.log(res.data.data)
      setData(res.data.data)
    })
  }, [])
  
  return (
    <Container>
      <Navbar>
        <NavbarInner>
          <h2>Matchmaking MMR</h2>
        </NavbarInner>
      </Navbar>
      <ContentContainer>
        <SideBar>
          <List>
            <ListItem>
              <p>Testing</p>
            </ListItem>
            <ListItem>
              <p>Testing</p>
            </ListItem>
          </List>
        </SideBar>
        <InnerContentContainer>
          <h2>MMR Rankings</h2>
          {data && 
            data.map(item => {
              return (
                <Row>
                  <p>{item.person}</p>
                  <p>{item.mmr.mmr}</p>
                </Row>
              )
            })
          }
        </InnerContentContainer>

      </ContentContainer>
    </Container>
  );
}

export default App;
