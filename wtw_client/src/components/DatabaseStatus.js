function DatabaseStatus(props) {
  const getStatusColor = () => {
    if (props.status.toLowerCase() === "started") {
      return "#11de11";
    } else {
      return "#fc152b";
    }
  };

  const capitalize = (str) => {
    return str.charAt(0).toUpperCase() + str.slice(1);
  };

  return (
    <div>
      <p>
        Database status:{" "}
        <span style={{ color: getStatusColor() }}>
          {capitalize(props.status)}
        </span>
      </p>
    </div>
  );
}
export default DatabaseStatus;
