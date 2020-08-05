import React from 'react';
import logo from './logo.svg';
import './App.css';
import { List, ListItem, Container, Navbar, NavbarInner, ContentContainer, SideBar, InnerContentContainer } from './styles'

const App = () => {
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

          <p>blah blah blah datatable here</p>
        </InnerContentContainer>

      </ContentContainer>
    </Container>
  );
}

export default App;
