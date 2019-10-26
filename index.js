var AWS = require('aws-sdk');
var pinpoint = new AWS.Pinpoint({region: process.env.region});
var projectId = process.env.projectId;
var originationNumber = process.env.originationNumber;
var grade_message = "An assignment grade has been changed in your course. Login to canvas to see your recent feedback!";
var announcement_message = "One of your instructors has posted an announcement in one of your courses. Login to canvas to view it!";
var assignment_message = "An assignment has been added to one of your classes! Login to canvas to view it!"
var quiz_message = "A quiz has been added to one of your classes! Login to canvas to view it!"

var messageType = "TRANSACTIONAL";
var message;

exports.handler = (event, context, callback) => {
  console.log('Received event:', event);
  if (event.source === "Grade Change") {
      message = grade_message;
  } else if (event.source === "New Announcement") {
    message = announcement_message;
  } else if (event.source === "New Assignment") {
    message = assignment_message;
  } else if (event.source === "New Quiz") {
    message = quiz_message;
  }
  validateNumber(event);
};

function validateNumber (event) {
  var destinationNumber = event.destinationNumber;
  if (destinationNumber.length === 10) {
    destinationNumber = "+1" + destinationNumber;
  }
  var params = {
    NumberValidateRequest: {
      IsoCountryCode: 'US',
      PhoneNumber: destinationNumber
    }
  };
  pinpoint.phoneNumberValidate(params, function(err, data) {
    if (err) {
      console.log(err, err.stack);
    }
    else {
      console.log(data);
      //return data;
      if (data['NumberValidateResponse']['PhoneTypeCode'] === 0) {
        createEndpoint(data, event.firstName, event.lastName, event.source);
      } else {
        console.log("Received a phone number that isn't capable of receiving "
                   +"SMS messages. No endpoint created.");
      }
    }
  });
}

function createEndpoint(data, firstName, lastName, source) {
  var destinationNumber = data['NumberValidateResponse']['CleansedPhoneNumberE164'];
  var endpointId = data['NumberValidateResponse']['CleansedPhoneNumberE164'].substring(1);

  var params = {
    ApplicationId: projectId,
    EndpointId: endpointId,
    EndpointRequest: {
      ChannelType: 'SMS',
      Address: destinationNumber,
      OptOut: 'ALL',
      Location: {
        PostalCode:data['NumberValidateResponse']['ZipCode'],
        City:data['NumberValidateResponse']['City'],
        Country:data['NumberValidateResponse']['CountryCodeIso2'],
      },
      Demographic: {
        Timezone:data['NumberValidateResponse']['Timezone']
      },
      Attributes: {
        Source: [
          source
        ]
      },
      User: {
        UserAttributes: {
          FirstName: [
            firstName
          ],
          LastName: [
            lastName
          ]
        }
      }
    }
  };
  pinpoint.updateEndpoint(params, function(err,data) {
    if (err) {
      console.log(err, err.stack);
    }
    else {
      console.log(data);
      //return data;
      sendConfirmation(destinationNumber);
    }
  });
}

function sendConfirmation(destinationNumber) {

  var params = {
    ApplicationId: projectId,
    MessageRequest: {
      Addresses: {
        [destinationNumber]: {
          ChannelType: 'SMS'
        }
      },
      MessageConfiguration: {
        SMSMessage: {
          Body: message,
          MessageType: messageType,
          OriginationNumber: originationNumber
        }
      }
    }
  };

  pinpoint.sendMessages(params, function(err, data) {
    if(err) {
      console.log(err.message);
    } else {
      console.log("Message sent! "
          + data['MessageResponse']['Result'][destinationNumber]['StatusMessage']);
    }
  });
}