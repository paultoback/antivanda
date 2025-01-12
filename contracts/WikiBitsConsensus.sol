// contracts/WikiBitsConsensus.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract WikiBitsConsensus {
    struct Edit {
        string articleId;
        string editHash;
        uint256 timestamp;
        string status;
        uint256 approvalCount;
        uint256 rejectionCount;
        address submitter;
        mapping(address => bool) hasVoted;
    }

    mapping(string => Edit) public edits;
    mapping(address => uint256) public editorReputations;
    
    uint256 public constant MINIMUM_VOTES_REQUIRED = 3;
    uint256 public constant APPROVAL_THRESHOLD = 70;

    event EditSubmitted(string editHash, string articleId, address submitter);
    event EditVoted(string editHash, address voter, bool approved);
    event EditFinalized(string editHash, bool approved);

    function submitEdit(string memory editHash, string memory articleId) public {
        require(edits[editHash].timestamp == 0, "Edit already exists");
        
        Edit storage newEdit = edits[editHash];
        newEdit.articleId = articleId;
        newEdit.editHash = editHash;
        newEdit.timestamp = block.timestamp;
        newEdit.status = "pending";
        newEdit.submitter = msg.sender;
        
        emit EditSubmitted(editHash, articleId, msg.sender);
    }

    function voteOnEdit(string memory editHash, bool approve) public {
        Edit storage edit = edits[editHash];
        require(edit.timestamp > 0, "Edit does not exist");
        require(!edit.hasVoted[msg.sender], "Already voted");
        require(keccak256(bytes(edit.status)) == keccak256(bytes("pending")), "Edit not pending");

        edit.hasVoted[msg.sender] = true;
        
        if (approve) {
            edit.approvalCount++;
        } else {
            edit.rejectionCount++;
        }

        emit EditVoted(editHash, msg.sender, approve);

        if (edit.approvalCount + edit.rejectionCount >= MINIMUM_VOTES_REQUIRED) {
            finalizeEdit(editHash);
        }
    }

    function finalizeEdit(string memory editHash) internal {
        Edit storage edit = edits[editHash];
        uint256 totalVotes = edit.approvalCount + edit.rejectionCount;
        uint256 approvalPercentage = (edit.approvalCount * 100) / totalVotes;
        
        bool approved = approvalPercentage >= APPROVAL_THRESHOLD;
        edit.status = approved ? "approved" : "rejected";
        
        if (approved) {
            editorReputations[edit.submitter]++;
        }
        
        emit EditFinalized(editHash, approved);
    }

    function getEditStatus(string memory editHash) public view returns (string memory) {
        return edits[editHash].status;
    }

    function getEditorReputation(address editor) public view returns (uint256) {
        return editorReputations[editor];
    }
}