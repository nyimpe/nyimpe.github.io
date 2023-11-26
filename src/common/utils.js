import _ from "lodash";

export const isEmptyValue = (value) => {
  return _.isEmpty(value);
};
