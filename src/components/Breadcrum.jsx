import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { KeyboardArrowRight } from "@mui/icons-material";
import { emphasize, styled } from "@mui/material/styles";
import { Box, Breadcrumbs, Chip } from "@mui/material";

const StyledBreadcrumb = styled(Chip)(({ theme }) => {
  const backgroundColor =
    theme.palette.mode === "light"
      ? theme.palette.grey[100]
      : theme.palette.grey[800];
  return {
    cursor: "pointer",
    backgroundColor,
    height: theme.spacing(3),
    maxWidth: 200,
    color: theme.palette.text.primary,
    fontWeight: theme.typography.fontWeightRegular,
    "&:hover, &:focus": {
      backgroundColor: emphasize(backgroundColor, 0.06),
    },
    "&:active": {
      boxShadow: theme.shadows[1],
      backgroundColor: emphasize(backgroundColor, 0.12),
    },
  };
});

const Breadcrum = () => {
  const { pathname } = useLocation();
  const [crumbs, setCrumbs] = useState([]);

  useEffect(() => {
    const path = [];
    pathname.split("/").forEach((item) => {
      if (item !== "") {
        path.push(item.toUpperCase());
      }
    });
    setCrumbs(pathname === "/" ? ["HOME"] : path);
  }, [pathname]);

  return (
    <Box sx={{ mt: 2, width: "100%" }}>
      <Breadcrumbs separator={<KeyboardArrowRight />}>
        {crumbs.map((e) => (
          <StyledBreadcrumb key={e} component="span" label={e} />
        ))}
      </Breadcrumbs>
    </Box>
  );
};

export default Breadcrum;
