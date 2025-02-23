import React from "react";

export default function ActorListItem(props) {
  return (
    <div>
      <div>
        <strong>
          {props.actor.name} {props.actor.surname}
        </strong>
        <button
          onClick={props.onDelete}
          style={{ marginLeft: "10px", color: "red" }}
        >
          Delete
        </button>
      </div>
    </div>
  );
}
