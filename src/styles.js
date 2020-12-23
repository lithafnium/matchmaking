import styled from 'styled-components'

export const Container = styled.div`
    min-height: 100vh; 
    width: 100%; 
`

export const Navbar = styled.div`
    position: fixed; 
    width: 100%; 
    height: 80px; 
    background-color: #d1363a;
    box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
    display: flex; 
    justify-content: center; 
    z-index: 10; 
    padding-left: 1rem; 
    padding-right: 1rem; 
`

export const NavbarInner = styled.div`
    width: 100%; 
    display: flex; 
    align-items: center; 
    
    h1, h2, h3, p {
        color: white; 
    }
`

export const ContentContainer = styled.div`
    width: 100%; 
    height: 100vh;
    display: flex; 
    z-index: 5; 
`

export const SideBar = styled.div`
    padding-top: 100px; 
    position: fixed; 
    width: 300px; 
    height: 100%; 
    box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
`

export const InnerContentContainer = styled.div`
    margin-left: 300px; 
    width: calc(100% - 300px);
    min-height: 100vh; 
    padding-top: 100px;
    padding-bottom: 2rem; 
    padding-left: 2rem; 
    padding-right: 2rem; 
`

export const List = styled.div`
    width: 100%; 
`
export const ListItem = styled.div`
    padding: 1rem; 

    background-position: center;
  transition: background 0.8s;
    
    & p {
        margin: 0px; 
    }

    &:hover{
        background: #dddddd radial-gradient(circle, transparent 1%, #dddddd 1%) center/15000%;
    }

    &:active {
      background-color: whitesmoke;
      background-size: 100%;
      transition: background 0s;
    }
`

export const Row = styled.div`
    width: 80%; 
    display: flex; 
    justify-content: space-between; 
`