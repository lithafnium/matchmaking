import React, { useEffect, useState } from 'react';
import logo from './logo.svg';
import './App.css';
import axios from 'axios'
import { List, ListItem, Container, Navbar, NavbarInner, ContentContainer, SideBar, InnerContentContainer } from './styles'

const App = () => {
  const [time, setTime] = useState(null)
  useEffect(() => {
    fetch('http://127.0.0.1:5000/time').then(res => res.json()).then(data => {
      setTime(data.time)
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

          <p>Time: {time}</p>
        </InnerContentContainer>

      </ContentContainer>
    </Container>
  );
}

export default App;
