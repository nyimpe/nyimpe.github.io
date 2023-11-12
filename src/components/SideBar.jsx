import { useNavigate } from "react-router-dom";

import Info from "@mui/icons-material/Info";
import OpenInNew from "@mui/icons-material/OpenInNew";
import HomeIcon from "@mui/icons-material/Home";
import img from "../assets/images/cat-pixel.jpeg";
import {
  Avatar,
  Divider,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  Typography,
} from "@mui/material";

const SideBar = () => {
  const navigate = useNavigate();
  return (
    <Drawer
      sx={{
        width: 250,
        flexShrink: 0,
        "& .MuiDrawer-paper": {
          width: 250,
          boxSizing: "border-box",
        },
      }}
      variant="permanent"
      anchor="left"
    >
      <List>
        <ListItem
          sx={{
            display: "flex",
            flexDirection: "column",
            gap: 3,
            mt: 3,
            width: "100%",
          }}
        >
          <Avatar src={img} sx={{ width: 150, height: 150 }} />
          <Typography variant="h5">김초밥</Typography>
          <Typography variant="h5">Description</Typography>
        </ListItem>
        <ListItem>
          <ListItemButton onClick={() => navigate("/")}>
            <ListItemIcon>
              <HomeIcon />
            </ListItemIcon>
            Home
          </ListItemButton>
        </ListItem>
        <ListItem>
          <ListItemButton onClick={() => navigate("/about")}>
            <ListItemIcon>
              <Info />
            </ListItemIcon>
            About
          </ListItemButton>
        </ListItem>
        <Divider />
        <ListItem>
          <ListItemButton component="a" href="#actionable">
            <ListItemIcon>
              <OpenInNew />
            </ListItemIcon>
            Javascript
          </ListItemButton>
        </ListItem>
      </List>
    </Drawer>
  );
};

export default SideBar;
