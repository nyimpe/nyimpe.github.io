import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Layout from "./layouts/Layout";
import ListPage from "./pages/ListPage";
import DetailPage from "./pages/DetailPage";
import RealEstate from "./pages/RealEstate";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    children: [
      {
        path: "/",
        element: <RealEstate />,
      },
      {
        path: ":category",
        element: <ListPage />,
      },
      {
        path: ":category/:id",
        element: <DetailPage />,
      },
    ],
  },
]);

const App = () => {
  return <RouterProvider router={router} />;
};

export default App;
