import React, { useEffect, useState } from 'react';
import logo from './logo.svg';
import './App.css';
import axios from 'axios'
import { List, ListItem, Container, Navbar, NavbarInner, ContentContainer, SideBar, InnerContentContainer } from './styles'
import DataTable from 'react-data-table-component'
const App = () => {
  const [data, setData] = useState(null)
  useEffect(() => {
    axios.get('http://127.0.0.1:5000/get_mmr').then(res => {
      console.log(res.data)
      setData(res.data)
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
          <h2>AARON</h2>
          {data && 
            data.aaron.map(row => {
              return <p>{row.mmr}</p>
            })}
          {/* {data && <DataTable
            columns={['mmr']}
            title="MMR"
            data={data.aaron}/>} */}

          
        </InnerContentContainer>

      </ContentContainer>
    </Container>
  );
}

export default App;
